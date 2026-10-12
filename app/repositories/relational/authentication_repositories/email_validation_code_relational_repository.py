from app.repositories.interfaces.authentication_repositories_interfaces.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface
from app.repositories.relational.authentication_repositories.password_recovery_token_relational_repository import \
    PasswordRecoveryTokenRelationalRepository
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class EmailValidationCodeRelationalRepository(BaseRelationalRepository, EmailValidationCodeRepositoryInterface, PasswordRecoveryTokenRelationalRepository):
    async def revoke_email_validation_code(self, email_validation_code_id: str):
        return await super().revoke_password_recovery_token(email_validation_code_id)
