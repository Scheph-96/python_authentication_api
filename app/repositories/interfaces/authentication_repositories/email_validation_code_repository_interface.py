class EmailValidationCodeRepositoryInterface:
    async def invalidate_code(self, email_validation_code_id: str):
        pass
