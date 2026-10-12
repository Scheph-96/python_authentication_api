from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class PasswordRecoveryTokenRepositoryInterface(BaseRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        pass

    async def find_by_user_id(self, user_id: str):
        pass

    async def revoke_password_recovery_token(self, recovery_token_id: str):
        pass

    async def revoke_all_password_recovery_tokens(self, user_id: str):
        pass
