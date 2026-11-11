from uuid import UUID

from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class PasswordRecoveryTokenRepositoryInterface(BaseRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        pass

    async def find_by_user_id(self, user_id: UUID):
        pass

    async def revoke_password_recovery_token(self, password_recovery_token_id: UUID):
        pass

    async def revoke_all_password_recovery_tokens_by_user_id(self, user_id: UUID):
        pass
