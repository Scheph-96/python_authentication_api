from datetime import datetime

from fastapi import HTTPException

from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.core_model.authentication_model.email_validation_code_model import EmailValidationCode
from app.repositories.interfaces.authentication_repositories_interfaces.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface
from app.repositories.interfaces.authentication_repositories_interfaces.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface
from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface
from app.utils.app_jwt import hash_token
from app.utils.resources import code_generator


class EmailValidationCodeService:
    # The EmailValidationCodeRepositoryInterface only has one method
    def __init__(self, repo: EmailValidationCodeRepositoryInterface):
        self.repo = repo
        self.logger = get_logger("EmailValidationCodeService")

    async def create_email_validation_code(self, user_id: str):
        # Generate the recovery token
        raw_code = code_generator()
        print("RAW CODE: ", raw_code)
        # Hash the token
        code_hash = hash_token(raw_code)

        # Create the model
        email_validation_code = EmailValidationCode(user_id=str(user_id), code_hash=code_hash)
        email_validation_code_id = await self.repo.create(email_validation_code.to_dict())

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: Email Validation Code Created",
            user_id=str(user_id),
            code_hash=code_hash
        )

        return {"raw_code": raw_code, "email_validation_code_id": email_validation_code_id}

    async def invalidate_code(self, user_id: str, code: str):
        code_hash = hash_token(code)

        email_validation_code = await self.get({"user_id": user_id, "code_hash": code_hash})

        if not email_validation_code:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATION CODE NOT FOUND"
            )

            raise HTTPException(400, "Invalid Data")

        email_validation_code = EmailValidationCode(**email_validation_code)

        # Timezone info of timezone aware variable
        my_timezone = email_validation_code.expire_at.tzinfo
        # Current datetime for the timezone
        now = datetime.now(my_timezone)

        # Check token expiration
        if email_validation_code.expire_at < now:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATION CODE EXPIRED"
            )

            raise HTTPException(400, "Invalid Code")

        # Check whether was used or not
        if email_validation_code.revoked:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATION CODE USED"
            )

            raise HTTPException(400, "Invalid Code")

        await self.revoke_all_email_recovery_tokens(str(email_validation_code.user_id))

        return email_validation_code.user_id

    async def check_email_validation_code_integrity(self, user_id: str):

        # Retrieve validation code record
        email_validation_code = await self.get_by_user_id(str(user_id))
        email_validation_code = EmailValidationCode(
            **email_validation_code) if email_validation_code is not None else None

        # If the code is revoked block the request
        # If a code already exist for this user we let it be
        # Every existing code is revoked when a new one is verified and validate
        # And if not the expiration time index will delete it
        if email_validation_code and email_validation_code.revoked:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATE: CODE ALREADY USED"
            )
            raise HTTPException(400, "Unable to proceed")


    async def revoke_all_email_recovery_tokens(self, user_id: str):
        return await self.repo.revoke_all_email_recovery_tokens(user_id)

    async def get(self, data: dict):
        return await self.repo.find(data)

    async def get_by_hash(self, code_hash: str):
        return await self.repo.find_by_hash(code_hash)

    async def get_by_user_id(self, user_id: str):
        return await self.repo.find_by_user_id(user_id)

    async def update_code_email_validation_code(self, email_validation_code_id: str):
        await self.repo.revoke_email_validation_code(email_validation_code_id)

    async def delete_email_validation_code(self, email_validation_code_id):
        await self.repo.delete_one_by_id(email_validation_code_id)
