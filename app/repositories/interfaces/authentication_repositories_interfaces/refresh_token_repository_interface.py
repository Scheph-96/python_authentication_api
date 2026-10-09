from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class RefreshTokenRepositoryInterface(BaseRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        pass

    async def revoke(self, token_id: str, replaced_by: str = None):
        pass

    async def delete_expired_revoked(self):
        pass
