from app.repositories.interfaces.authentication_repositories.email_validation_code_repository_interface import \
    EmailValidationCodeRepositoryInterface


class RelationalEmailValidationCodeRepository(EmailValidationCodeRepositoryInterface):

    async def invalidate_code(self, email_validation_code_id: str):
        return await super().invalidate_code(email_validation_code_id)