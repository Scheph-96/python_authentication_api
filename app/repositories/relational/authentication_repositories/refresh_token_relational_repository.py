from app.repositories.interfaces.authentication_repositories_interfaces.refresh_token_repository_interface import \
    RefreshTokenRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class RefreshTokenRelationalRepository(BaseRelationalRepository, RefreshTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        pass

    async def revoke(self, token_id: str, replaced_by: str = None):
        pass

    async def delete_expired_revoked(self):
        pass
