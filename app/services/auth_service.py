from app.services.user_service import UserService
from app.services.refresh_token_service import RefreshTokenService
from app.services.password_recovery_token_service import PasswordRecoveryTokenService
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.utils.jwt import create_access_token, hash_token
from app.utils.email import email_processing
from fastapi import HTTPException, BackgroundTasks
from argon2.exceptions import VerifyMismatchError, InvalidHashError

"""
    Here lies all or authentication process. If we want to add other type of authentication it will be here
    
    The data here is safe to process, we already went through the sanitization and validation with the Schemas in the controller
"""


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        refresh_token_service: RefreshTokenService,
        base_repository: BaseRepository,
        password_recovery_token_service: PasswordRecoveryTokenService,
    ):
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service
        self.base_repository = base_repository
        self.password_recovery_token_service = password_recovery_token_service

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

        # If the request provide a username attribute, the login is performed with username
        if data.get("username"):
            user = await self.user_service.get_by_username(data["username"])

        # If the request provide a email attribute, the login is performed with the email
        elif data.get("email"):
            user = await self.user_service.get_by_email(data["email"])
        if not user:
            raise HTTPException(401, "Invalid credentials")

        user = User(**user)

        try:
            user.verify_password(data["password"])
        except VerifyMismatchError:
            raise HTTPException(401, "Invalid credentials")
        except InvalidHashError:
            print(user.to_dict())
            raise HTTPException(401, "Invalid credentials")

        access_token = create_access_token(str(user._id))
        refresh_token = await self.refresh_token_service.create_refresh_token(
            str(user._id)
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    """
        Validate users account by validating the code sent to their email address
    """

    async def validate_email(self, data: dict):
        # First we hash the code
        code_hash = hash_token(data.get("code"))

        # Now we compare the hashed code and the user with our database record
        email_validation_code = await self.base_repository.find(
            {"user_id": data.get("user_id"), "code_hash": code_hash}
        )

        # If there is no match reject the request
        if not email_validation_code:
            raise HTTPException(400, "Invalid or expired code")

        # If there is a match we delete code record
        await self.base_repository.delete(email_validation_code["_id"])

        # And finally we update the user status
        await self.user_service.update_user(data.get("user_id"), {"is_verified": True})

        return {"status": "verified"}

    """
        Users can request a new code that will be sent to their email address
    """

    async def resend_validate_email(
        self, data: dict, background_tasks: BackgroundTasks
    ):

        # Check whether the user exist
        user = await self.user_service.get_by_id(data.get("user_id"))

        # If the user does not exist, reject the request
        if not user:
            raise HTTPException(400, "Unable to proceed")

        # Get the validation code record
        email_validation_code = await self.base_repository.find(
            {"user_id": str(user["_id"])}
        )

        # If there is a validation code with the provided user id, delete it
        if email_validation_code:
            await self.base_repository.delete(str(email_validation_code["_id"]))

        user = User(**user)

        # Send email to validate the user email address in background
        background_tasks.add_task(email_processing, user, self.base_repository)

        return "Email Resent"

    async def password_recovery_confirm_email(self, data: dict):
        user = await self.user_service.get_by_email(data["email"])

        if not user:
            # Do not reveal whether the email exists
            raise HTTPException(400, "If this email exists, a reset link has been sent")
        
        # Insert the hashed token in the database
        password_recovery_token = await self.password_recovery_token_service.create_password_recovery_token(str(user["_id"]))

        return {"password_recovery_token": password_recovery_token}

    async def password_recovery_update_password(self, data: dict):
        pass
