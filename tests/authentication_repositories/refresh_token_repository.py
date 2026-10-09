from app.repositories.interfaces.authentication_repositories.refresh_token_repository_interface import \
    RefreshTokenRepositoryInterface


class RelationalRefreshTokenRepository(RefreshTokenRepositoryInterface):
    async def find_by_hash(self, token_hash: str):
        return await super().find_by_hash(token_hash)

    async def revoke(self, token_id: str, replaced_by: str = None):
        return await super().revoke(token_id, replaced_by)

    async def delete_expired_revoked(self):
        return await super().delete_expired_revoked()