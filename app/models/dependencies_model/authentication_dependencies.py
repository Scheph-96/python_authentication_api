from fastapi import BackgroundTasks

from app.services.core_services.authentication.model_services.email_validation_code_service import EmailValidationCodeService
from app.services.core_services.authentication.model_services.password_recovery_token_service import PasswordRecoveryTokenService
from app.services.core_services.authentication.model_services.refresh_token_service import RefreshTokenService
from app.services.core_services.authentication.model_services.user_service import UserService


class AuthenticationDependencies:
    def __init__(self,
                 user_service: UserService,
                 refresh_token_service: RefreshTokenService,
                 password_recovery_token_service: PasswordRecoveryTokenService,
                 email_validation_code_service: EmailValidationCodeService,
                 background_tasks: BackgroundTasks):
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service
        self.password_recovery_token_service = password_recovery_token_service
        self.email_validation_code_service = email_validation_code_service
        self.background_tasks = background_tasks
