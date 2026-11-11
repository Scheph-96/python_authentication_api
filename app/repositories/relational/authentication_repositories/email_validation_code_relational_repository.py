from uuid import UUID

from app.repositories.interfaces.authentication_repositories_interfaces.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface
from app.repositories.relational.authentication_repositories.password_recovery_token_relational_repository import \
    PasswordRecoveryTokenRelationalRepository

# BaseDocumentRepository is not inherited here because it already is in PasswordRecoveryTokenDocumentRepository
# If we try to inherit it anyway it will trigger a TypeError
# Cannot create a consistent method resolution order (MRO)
# Because PasswordRecoveryTokenDocumentRepository already inherit BaseDocumentRepository
class EmailValidationCodeRelationalRepository(PasswordRecoveryTokenRelationalRepository, EmailValidationCodeRepositoryInterface):
    async def revoke_email_validation_code(self, email_validation_code_id: UUID):
        return await super().revoke_password_recovery_token(email_validation_code_id)

    async def revoke_all_email_recovery_tokens(self, user_id: UUID):
        return await super().revoke_all_password_recovery_tokens_by_user_id(user_id)
