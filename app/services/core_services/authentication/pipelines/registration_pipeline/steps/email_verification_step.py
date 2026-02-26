from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.database.motor import db
from app.models.core_model.email_validation_code_model import EmailValidationCode
from app.repositories.base_repository import BaseRepository
from app.services.Infrastructure.email_service import EmailService
from app.services.model_services.email_validation_code_service import EmailValidationCodeService
from app.utils.jwt import hash_token
from app.utils.resources import code_generator


class EmailVerificationStep:
    def __init__(self, email_service: EmailService, email_validation_code_service: EmailValidationCodeService):
        self.email_service = email_service
        self.email_validation_code_service = email_validation_code_service
        self.logger = get_logger("EmailVerificationStep")

    async def run(self, ctx):
        # Generate validation code
        result = await self.email_validation_code_service.create_email_validation_code(ctx.user._id)

        # Create email validation record schema
        email_validation_code = EmailValidationCode(
            user_id=str(ctx.user._id), code_hash=hash_token(result["raw_code"])
        )

        # Send email with the validation code
        await self.email_service.send(
            to=ctx.user.email,
            subject="Email Validation",
            text=self.email_service.verification_email_template_plain_text(result["raw_code"]),
            html=self.email_service.verification_email_template_html(result["raw_code"]),
        )

        self.logger.info(
            f"{Settings.OPERATION_SUCCESS_EVENT_LABEL}: email_sent",
            user_id=str(ctx.user._id),
            email_validation_code_id=result["email_validation_code_id"],
        )