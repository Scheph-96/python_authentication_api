from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class EmailValidationCodeRepositoryInterface(BaseRepositoryInterface):
    async def revoke_email_validation_code(self, email_validation_code_id: str):
        pass
