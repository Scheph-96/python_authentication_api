from app.repositories.document.authentication_repositories.password_recovery_token_repository import \
    PasswordRecoveryTokenRepository


class EmailValidationCodeRepository(PasswordRecoveryTokenRepository):
    async def invalidate_code(self, email_validation_code_id: str):
        return await super().invalidate_token(email_validation_code_id)
