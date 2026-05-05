from app.core.config import Settings
from app.models.dependencies_model.authentication_dependencies import AuthenticationDependencies
from app.services.Infrastructure.email_service import EmailService
from app.services.Infrastructure.pipeline_tasks import \
    PipelineTasks
# from app.services.core_services.authentication.pipelines.registration_pipeline.steps.assign_role_step import \
#     RoleAssignmentStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.email_validation_step import \
    EmailVerificationStep
from app.services.core_services.authentication.pipelines.registration_pipeline.steps.user_creation_step import \
    UserCreationStep


def build_registration_pipeline(auth_depends: AuthenticationDependencies):
    """
        The factory is meant to activate or deactivate each feature of registration process

        Currently, when Password Hash -> Data insertion -> Email Validation -> Set authorization

        In some case, depending on the project we might not want a too complex registration
        process, we might just want to receive users data hash password and save. So in that
        scenario the steps list will only contain UserCreationStep.

        To activate or deactivate a feature go app.core.config in the Settings set
        EMAIL_VALIDATION to true to activate or false to deactivate email validation
        ROLE_ASSIGNMENT to true to activate or false to deactivate role assignment
    """

    steps = [UserCreationStep(auth_depends=auth_depends)]

    if Settings.EMAIL_VALIDATION:
        steps.append(EmailVerificationStep(auth_depends=auth_depends, email_service=EmailService()))

    if Settings.ROLE_ASSIGNMENT:
        # steps.append(RoleAssignmentStep())
        pass

    return PipelineTasks(steps)