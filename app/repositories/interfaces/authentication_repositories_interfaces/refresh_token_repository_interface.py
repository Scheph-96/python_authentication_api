from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class RefreshTokenRepositoryInterface(BaseRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        pass

    async def revoke(self, token_id: str, new_refresh_token: str = None):
        pass

    async def revoke_and_expire_all_refresh_tokens_by_user(self, user_id: str):
        pass

    async def delete_expired_revoked(self):
        pass
