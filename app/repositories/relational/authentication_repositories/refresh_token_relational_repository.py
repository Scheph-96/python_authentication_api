from app.repositories.interfaces.authentication_repositories_interfaces.refresh_token_repository_interface import \
    RefreshTokenRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class RefreshTokenRelationalRepository(BaseRelationalRepository, RefreshTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        pass

    async def revoke(self, token_id: str, new_refresh_token: str | None = None):
        pass

    async def revoke_and_expire_all_refresh_tokens_by_user(self, user_id: str):
        pass

    async def delete_expired_revoked(self):
        pass
