from app.core.logging.logger import get_logger
from app.core.config import Settings
from app.services.model_schema_services.user_service import UserService
from app.services.model_schema_services.refresh_token_service import RefreshTokenService
from app.services.model_schema_services.password_recovery_token_service import PasswordRecoveryTokenService
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.utils.jwt import create_access_token, hash_token
from app.utils.email_process import email_processing
from fastapi import HTTPException, BackgroundTasks
from argon2.exceptions import VerifyMismatchError, InvalidHashError

"""
    Here lies all or authentication process. If we want to add other type of authentication it will be here
    
    The data here is safe to process, we already went through the sanitization and validation with the Schemas in the controller
"""


class AuthenticationService:

    def __init__(
        self,
        user_service: UserService,
        refresh_token_service: RefreshTokenService,
        password_recovery_token_service: PasswordRecoveryTokenService,
        email_validation_repository: BaseRepository
    ):
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service
        self.password_recovery_token_service = password_recovery_token_service
        self.email_validation_repository = email_validation_repository
        self.logger = get_logger("AuthenticationService")

    """
        Create an account for the user
    """

    async def user_registration(self, data: dict, background_tasks: BackgroundTasks):

        # One email per user, no duplication
        if await self.user_service.get_by_email(data["email"]):
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail=f"EMAIL {data["email"]} ALREADY EXIST"
            )

            raise HTTPException(400, "Invalid Credential")

        # Unique username
        if await self.user_service.get_by_username(data["username"]):
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail=f"USERNAME {data["username"]} ALREADY EXIST"
            )

            raise HTTPException(400, "Invalid Credential")

        user = User(username=data["username"], email=data["email"])

        # This method hash the password
        user.set_password(data["password"])

        # Create user and get the id
        user_id = await self.user_service.create_user(user.to_dict())
        user._id = user_id

        # Send email to validate the user email address in background
        background_tasks.add_task(email_processing, user, self.email_validation_repository)

        self.logger.info(
            Settings.SECURITY_EVENT_LABEL,
            detail=f"USER CREATED SUCCESSFULLY",
            user_id=str(user._id)
        )

        # retrieve user id
        return user._id

    """
        Authenticate a user
        
        We want to log our users in whether with the 
        email or the username

        Raises:
            HTTPException: the request body has to contain email or username otherwise the request is rejected
            
            HTTPException: if no record match with the provided data we reject the request. No user match thus invalid email or username
            
            HTTPException: password verification failed. Invalid password
    """

    async def login(self, data: dict):

        user = None

        # If the request provide a username attribute, the login is performed with username
        if data.get("username"):
            user = await self.user_service.get_by_username(data["username"])

        # If the request provide a email attribute, the login is performed with the email
        elif data.get("email"):
            user = await self.user_service.get_by_email(data["email"])

        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL, detail="INCORRECT EMAIL OR PASSWORD"
            )

            raise HTTPException(401, "Invalid credentials")

        user = User(**user)

        try:
            user.verify_password(data["password"])
        except VerifyMismatchError:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="THE SECRET DOES NOT MATCH THE HASH",
            )

            raise HTTPException(401, "Invalid credentials")
        except InvalidHashError:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="THE HASH IS INVALIDE. EXPIRED OR WRONG ISSUER",
            )

            raise HTTPException(401, "Invalid credentials")

        access_token = create_access_token(str(user._id))
        result = await self.refresh_token_service.create_refresh_token(str(user._id))

        self.logger.info(
            "user_login",
            user_id=str(user._id),
            refresh_token_id=str(result["refresh_token_id"]),
        )

        return {"access_token": access_token, "refresh_token": result["raw_token"]}

    """
        Validate users account by validating the code sent to their email address
    """

    async def refresh_token(self, data: dict):

        refresh_token = await self.refresh_token_service.is_refresh_token_valid(data["refresh_token"])

        user_id = str(refresh_token.user_id)

        # ROTATE
        # Generate new refresh token
        new_refresh = await self.refresh_token_service.create_refresh_token(user_id)

        new_hash = hash_token(new_refresh["raw_token"])

        # Revoke the old token
        await self.refresh_token_service.update_refresh_token(refresh_token._id, new_hash)

        # Generate new access token
        new_access = create_access_token(user_id)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh["raw_token"],
        }

    async def validate_verification_code(self, data: dict):
        """
            This function is used to validate the code users send to verify their email
        """
        # First we hash the code
        code_hash = hash_token(data.get("code"))

        # Now we compare the hashed code and the user with our database record
        email_validation_code = await self.email_validation_repository.find(
            {"user_id": data.get("user_id"), "code_hash": code_hash}
        )

        # If there is no match reject the request
        if not email_validation_code:
            raise HTTPException(400, "Invalid or expired code")

        # If there is a match we delete code record
        await self.email_validation_repository.delete(email_validation_code["_id"])

        # And finally we update the user status
        await self.user_service.update_user(data.get("user_id"), {"is_verified": True})

        return {"status": "verified"}

    """
        Users can request a new code that will be sent to their email address
    """

    async def resend_validation_code(
        self, data: dict, background_tasks: BackgroundTasks
    ):
        """
            When the user want a new validation code
        """

        # Check whether the user exist
        user = await self.user_service.get_by_id(data["user_id"])

        # If the user does not exist, reject the request
        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL SENDING: THERE IS NO RECORD FOR THE SPECIFIED USER ID IN USER COLLECTION",
            )
            raise HTTPException(400, "Unable to proceed")

        if user["is_verified"]:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL SENDING: USER ALREADY VERIFIED"
            )
            raise HTTPException(400, "Unable to proceed")

        # Get the validation code record
        email_validation_code = await self.email_validation_repository.find(
            {"user_id": str(user["_id"])}
        )

        # If there is a validation code with the provided user id, delete it
        if email_validation_code:
            await self.email_validation_repository.delete(str(email_validation_code["_id"]))

        user = User(**user)

        # Send email to validate the user email address in background
        background_tasks.add_task(email_processing, user, self.email_validation_repository)

        return "Email Resent"

    """
        Users provide an email to recover their account and update the password.
        First, we confirm the email and return the recovery process token
    """

    async def password_recovery_confirm_email(self, data: dict):
        user = await self.user_service.get_by_email(data["email"])

        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="PASSWORD RECOVERY: EMAIL VALIDATION FAILED",
            )

            # Do not reveal whether the email exists
            raise HTTPException(400, "If this email exists, a reset link has been sent")

        # Insert the hashed token in the database
        result = (
            await self.password_recovery_token_service.create_password_recovery_token(
                str(user["_id"])
            )
        )

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: password_recovery_token_issued",
            user_id=str(
                user["_id"],
            ),
            password_recovery_token_id=result["password_recovery_token_id"],
        )

        return {"password_recovery_token": result["raw_token"]}

    """
        Second, we receive the token with new password. The token is then marked as used
        and we update user's password
    """

    async def password_recovery_reset_password(self, data: dict):
        # Get the user id
        user_id = await self.password_recovery_token_service.invalidate_token(
            data["token"]
        )

        # Get users data
        user = await self.user_service.get_by_id(str(user_id))

        # Hash the password
        user = User(**user)
        user.set_password(data["new_password"])

        # Increment auth_version
        user.auth_version += 1

        # Reset the password
        await self.user_service.update_user(
            user_id,
            {
                "hashed_password": user.hashed_password,
                "auth_version": user.auth_version,
            },
        )

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: password_updated",
            user_id=str(user_id),
            auth_version=str(user.auth_version),
        )

        return {"message": "Password updated successfully"}

    """
        Users login, they have to logout
    """

    async def logout(self, data: dict):
        refresh_token = await self.refresh_token_service.is_refresh_token_valid(
            data["refresh_token"]
        )

        # Increment authentication version
        await self.user_service.update_inc_user(
            refresh_token.user_id, {"auth_version": 1}
        )

        # Revoke refresh_token
        await self.refresh_token_service.update_refresh_token(refresh_token._id)

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: user_logout",
            user_id=str(refresh_token.user_id),
            refresh_token_id=str(refresh_token._id),
        )

        return {"logged_out": True}
