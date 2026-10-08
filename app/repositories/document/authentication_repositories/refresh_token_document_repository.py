from datetime import datetime, timezone
from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authentication_repositories_interfaces.refresh_token_repository_interface import \
    RefreshTokenRepositoryInterface


class RefreshTokenDocumentRepository(BaseDocumentRepository, RefreshTokenRepositoryInterface):

    async def find_by_hash(self, token_hash: str):
        return await self._collection.find_one({"token_hash": token_hash})

    async def revoke(self, token_id: str, replaced_by: str = None):
        await self._collection.update_one({"_id": UUID(token_id)},
                                          {"$set": {"revoked": True, "replaced_by": replaced_by}})

    async def delete_expired_revoked(self):
        await self._collection.delete_many({
            "revoke": True,
            "expires_at": {"$lt": datetime.now(timezone.utc)}
        })
