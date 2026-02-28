from app.core.config import Settings
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.services.Infrastructure.email_service import EmailService
from app.services.Infrastructure.feature_step import FeatureStep
from app.services.core_services.authentication.pipelines.registration_pipeline.registration_pipeline import \
    RegistrationPipeline
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.assign_role_step import AssignRoleStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.email_verification_step import \
    EmailVerificationStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.user_creation_step import \
    UserCreationStep


# Update auth_depends and define all the required services to pass them to this function
def build_registration_pipeline(auth_depends: AuthenticationDependencies):
    steps = [UserCreationStep(auth_depends=auth_depends)]

    if Settings.EMAIL_VERIFICATION:
        steps.append(EmailVerificationStep(auth_depends=auth_depends, email_service=EmailService()))

    if Settings.ROLE_ASSIGNMENT:
        # steps.append(AssignRoleStep())
        pass

    return RegistrationPipeline(steps)