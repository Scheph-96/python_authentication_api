from argon2.exceptions import VerifyMismatchError, InvalidHashError
from fastapi import HTTPException, BackgroundTasks

from app.core.config import Settings
from app.core.factories.authentication_factory import build_registration_pipeline
from app.core.logging.logger import get_logger
from app.models.core_model.authentication_model.email_validation_code_model import EmailValidationCode
from app.models.core_model.authentication_model.user_model import User
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.models.pipelines_context.registration_context import RegistrationContext
from app.services.Infrastructure.email_service import EmailService
from app.utils.jwt import create_access_token, hash_token


class AuthenticationService:
    """
        Here lies every authentication process.
        If we want to add other type of authentication it will be here

        The data here is safe to process,
        we already went through the sanitization
        and validation with the Schemas in the controller
    """

    def __init__(self, auth_depends: AuthenticationDependencies):
        self.auth_depends = auth_depends
        self.logger = get_logger("AuthenticationService")

    async def user_registration(self, data: dict):
        """
            Create an account for the user
        :param data: Request data
        :return: Created user id
        """

        # Initialize context attributes
        ctx = RegistrationContext(data)

        # Register all the steps
        registration_pipeline = build_registration_pipeline(self.auth_depends)

        # Run each step
        ctx = await registration_pipeline.run(ctx)

        return str(ctx.user._id)

    async def login(self, data: dict):
        """
            Authenticate a user. We want to log our users in whether with the
            email or the username

        :param data: Request data
        :return: access_token and refresh_token
        """

        user = None

        # If the request provide a username attribute, the login is performed with username
        if data.get("username"):
            user = await self.auth_depends.user_service.get_by_username(data["username"])

        # If the request provide an email attribute, the login is performed with the email
        elif data.get("email"):
            user = await self.auth_depends.user_service.get_by_email(data["email"])

        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL, detail="INCORRECT EMAIL OR USERNAME"
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
                detail="THE HASH IS INVALID. EXPIRED OR WRONG ISSUER",
            )

            raise HTTPException(401, "Invalid credentials")

        access_token = create_access_token(str(user._id), user.effective_permissions)
        result = await self.auth_depends.refresh_token_service.create_refresh_token(str(user._id))

        self.logger.info(
            "user_login",
            user_id=str(user._id),
            refresh_token_id=str(result["refresh_token_id"]),
        )

        return {"access_token": access_token, "refresh_token": result["raw_token"]}

    async def refresh_token(self, data: dict):
        """
            Validate users account by validating the code sent to their email address

        :param data: Request data
        :return: new access_token and new refresh_token
        """

        refresh_token = await self.auth_depends.refresh_token_service.is_refresh_token_valid(data["refresh_token"])

        user_id = str(refresh_token.user_id)

        # ROTATE
        # Generate new refresh token
        new_refresh = await self.auth_depends.refresh_token_service.create_refresh_token(user_id)

        new_hash = hash_token(new_refresh["raw_token"])

        # Revoke the old token
        await self.auth_depends.refresh_token_service.update_refresh_token(refresh_token._id, new_hash)

        # Generate new access token
        new_access = create_access_token(user_id)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh["raw_token"],
        }

    async def validate_verification_code(self, data: dict):
        """
            This function is used to validate the code users send to verify their email

        :param data: Request data
        :return: Confirmation String
        """

        # First we hash the code
        code_hash = hash_token(data.get("code"))

        # Now we compare the hashed code and the user with our database record
        email_validation_code = await self.auth_depends.email_validation_code_service.get(
            {"user_id": data.get("user_id"), "code_hash": code_hash}
        )
        email_validation_code = EmailValidationCode(
            **email_validation_code) if email_validation_code is not None else None

        # If there is no match reject the request
        if not email_validation_code:
            raise HTTPException(400, "Invalid or expired code")

        # The code is verified, we mark it as used
        await self.auth_depends.email_validation_code_service.invalidate_code_email_validation_code(
            str(email_validation_code._id))

        # And finally we update user status
        await self.auth_depends.user_service.update_user(data.get("user_id"), {"is_verified": True})

        return {"status": "verified"}

    async def resend_validation_code(self, data: dict):
        """
            Users can request a new code that will be sent to their email address

        :param data: Request data
        :return: Confirmation String
        """

        # Retrieve user data
        user = await self.auth_depends.user_service.get_by_id(data["user_id"])
        user = User(**user) if user is not None else None

        # If the user does not exist, reject the request
        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL SENDING: THERE IS NO RECORD FOR THE SPECIFIED USER ID IN USER COLLECTION",
            )
            raise HTTPException(400, "Unable to proceed")

        if user.is_verified:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL SENDING: USER ALREADY VERIFIED"
            )
            raise HTTPException(400, "Unable to proceed")

        # Retrieve validation code record
        email_validation_code = await self.auth_depends.email_validation_code_service.get_by_user_id(str(user._id))
        email_validation_code = EmailValidationCode(
            **email_validation_code) if email_validation_code is not None else None

        # If the code is marked as used block the request
        if email_validation_code and email_validation_code.is_used:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL SENDING: CODE ALREADY USED"
            )
            raise HTTPException(400, "Unable to proceed")

        email_service = EmailService()

        result = await self.auth_depends.email_validation_code_service.create_email_validation_code(str(user._id))

        # Send email to validate the user email address in background
        self.auth_depends.background_tasks.add_task(email_service.send, user.email, "Email Validation",
                                  email_service.verification_email_template_plain_text(result["raw_code"]),
                                  email_service.verification_email_template_html(result["raw_code"]))

        return {"status": "Email Resent"}

    async def password_recovery_confirm_email(self, data: dict):
        """
            Users provide an email to recover their account and update the password.
            First, we confirm the email and return the recovery process token

        :param data: Request data
        :return: password_recovery_token
        """

        user = await self.auth_depends.user_service.get_by_email(data["email"])
        user = User(**user) if user is not None else None

        if not user:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="PASSWORD RECOVERY: EMAIL VALIDATION FAILED",
            )

            # Do not reveal whether the email exists
            raise HTTPException(400, "If this email exists, a reset link has been sent")

        # Insert the hashed token in the database
        result = await self.auth_depends.password_recovery_token_service.create_password_recovery_token(str(user._id))

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: password_recovery_token_issued",
            user_id=str(user._id),
            password_recovery_token_id=result["password_recovery_token_id"],
        )

        return {"password_recovery_token": result["raw_token"]}

    async def password_recovery_reset_password(self, data: dict):
        """
            Second, we receive the token with new password. The token is then marked as used,
            and we update user's password
        :param data: Request data
        :return: Confirmation message
        """

        # Get the user id
        user_id = await self.auth_depends.password_recovery_token_service.invalidate_token(
            data["token"]
        )

        # Get users data
        user = await self.auth_depends.user_service.get_by_id(str(user_id))

        # Hash the password
        user = User(**user)
        user.set_password(data["new_password"])

        # Increment auth_version
        user.auth_version += 1

        # Reset the password
        await self.auth_depends.user_service.update_user(
            str(user._id),
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

        return {"status": "Password updated"}

    async def logout(self, data: dict):
        """
            Users login, they have to log out

        :param data: Request data
        :return:
        """

        refresh_token = await self.auth_depends.refresh_token_service.is_refresh_token_valid(
            data["refresh_token"]
        )

        # Increment authentication version
        await self.auth_depends.user_service.update_inc_user(
            refresh_token.user_id, {"auth_version": 1}
        )

        # Revoke refresh_token
        await self.auth_depends.refresh_token_service.update_refresh_token(refresh_token._id)

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: user_logout",
            user_id=str(refresh_token.user_id),
            refresh_token_id=str(refresh_token._id),
        )

        return {"status": "Logged Out"}
