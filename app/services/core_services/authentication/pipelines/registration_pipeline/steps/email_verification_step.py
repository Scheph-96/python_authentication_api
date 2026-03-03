from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.services.Infrastructure.email_service import EmailService
from app.models.dependencies_model.feature_step import FeatureStep


class EmailVerificationStep(FeatureStep):
    def __init__(self, auth_depends: AuthenticationDependencies, email_service: EmailService):
        self.email_service = email_service
        self.auth_depends = auth_depends
        self.logger = get_logger("EmailVerificationStep")

    async def run(self, ctx):
        # Send email to validate the user email address in background
        self.auth_depends.background_tasks.add_task(self.send_validation_email, ctx)
        return ctx

    async def send_validation_email(self, ctx):
        # Generate validation code
        result = await self.auth_depends.email_validation_code_service.create_email_validation_code(ctx.user._id)

        # Create email validation record schema
        # email_validation_code = EmailValidationCode(
        #     user_id=str(ctx.user._id), code_hash=hash_token(result["raw_code"])
        # )

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