from app.repositories.document.authentication_repositories.password_recovery_token_document_repository import \
    PasswordRecoveryTokenDocumentRepository
from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authentication_repositories_interfaces.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface


class EmailValidationCodeDocumentRepository(BaseDocumentRepository, EmailValidationCodeRepositoryInterface, PasswordRecoveryTokenDocumentRepository):
    async def invalidate_code(self, email_validation_code_id: str):
        return await super().invalidate_token(email_validation_code_id)
