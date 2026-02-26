from app.core.config import Settings
from app.services.Infrastructure.email_service import EmailService
from app.services.core_services.authentication.pipelines.registration_pipeline.registration_pipeline import \
    RegistrationPipeline
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.assign_role_step import AssignRoleStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.email_verification_step import \
    EmailVerificationStep

# Update auth_depends and define all the required services to pass them to this function
def build_registration_pipeline():
    steps = []

    if Settings.EMAIL_VERIFICATION:
        email_service = EmailService()
        steps.append(EmailVerificationStep(email_service=email_service))

    if Settings.ROLE_ASSIGNMENT:
        # steps.append(AssignRoleStep())
        pass

    return RegistrationPipeline(steps)