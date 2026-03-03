from app.core.config import Settings
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.services.Infrastructure.email_service import EmailService
from app.services.Infrastructure.feature_pipeline import \
    FeaturePipeline
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.email_verification_step import \
    EmailVerificationStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.user_creation_step import \
    UserCreationStep


def build_registration_pipeline(auth_depends: AuthenticationDependencies):
    steps = [UserCreationStep(auth_depends=auth_depends)]

    if Settings.EMAIL_VERIFICATION:
        steps.append(EmailVerificationStep(auth_depends=auth_depends, email_service=EmailService()))

    if Settings.ROLE_ASSIGNMENT:
        # steps.append(AssignRoleStep())
        pass

    return FeaturePipeline(steps)