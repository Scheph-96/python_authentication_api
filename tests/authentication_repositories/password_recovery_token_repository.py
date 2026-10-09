from app.repositories.interfaces.authentication_repositories.password_recovery_token_repository_interface import \
    PasswordRecoveryTokenRepositoryInterface


class RelationalPasswordRecoveryTokenRepository(PasswordRecoveryTokenRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        return await super().find_by_hash(token_hash)

    async def find_by_user_id(self, user_id: str):
        return await super().find_by_user_id(user_id)

    async def invalidate_token(self, recovery_token_id: str):
        return await super().invalidate_token(recovery_token_id)