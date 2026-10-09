from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class EmailValidationCodeRepositoryInterface(BaseRepositoryInterface):
    async def invalidate_code(self, email_validation_code_id: str):
        pass
