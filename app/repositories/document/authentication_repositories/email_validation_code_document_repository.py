from app.repositories.document.authentication_repositories.password_recovery_token_document_repository import \
    PasswordRecoveryTokenDocumentRepository
from app.repositories.interfaces.authentication_repositories_interfaces.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface

# BaseDocumentRepository is not inherited here because it already is in PasswordRecoveryTokenDocumentRepository
# If we try to inherit it anyway it will trigger a TypeError
# Cannot create a consistent method resolution order (MRO)
class EmailValidationCodeDocumentRepository(PasswordRecoveryTokenDocumentRepository, EmailValidationCodeRepositoryInterface):
    async def invalidate_code(self, email_validation_code_id: str):
        return await super().invalidate_token(email_validation_code_id)
