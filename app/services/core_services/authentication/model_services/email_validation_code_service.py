from datetime import datetime

from fastapi import HTTPException

from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.core_model.authentication_model.email_validation_code_model import EmailValidationCode
from app.repositories.authentication_repositories.email_validation_code_repository import EmailValidationCodeRepository
from app.utils.jwt import hash_token
from app.utils.resources import code_generator


class EmailValidationCodeService:
    def __init__(self, repo: EmailValidationCodeRepository):
        self.repo = repo
        self.logger = get_logger("EmailValidationCodeService")

    async def create_email_validation_code(self, user_id: str):
        # Generate the recovery token
        raw_code = code_generator()
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

    async def invalidate_code(self, code: str):
        code_hash = hash_token(code)

        email_validation_code = await self.repo.find_by_hash(code_hash)

        if not email_validation_code:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATION CODE NOT FOUND"
            )

            raise HTTPException(400, "Invalid Code")

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
        if email_validation_code.is_used:
            self.logger.warning(
                Settings.SECURITY_EVENT_LABEL,
                detail="EMAIL VALIDATION CODE USED"
            )

            raise HTTPException(400, "Invalid Code")

        await self.repo.invalidate_code(str(email_validation_code._id))

        return email_validation_code.user_id

    async def get(self, data: dict):
        return await self.repo.find(data)

    async def get_by_hash(self, code_hash: str):
        return await self.repo.find_by_hash(code_hash)

    async def get_by_user_id(self, user_id: str):
        return await self.repo.find_by_user_id(user_id)

    async def invalidate_code_email_validation_code(self, email_validation_code_id: str):
        await self.repo.invalidate_code(email_validation_code_id)

    async def delete_email_validation_code(self, email_validation_code_id):
        await self.repo.delete(email_validation_code_id)
