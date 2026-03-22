from datetime import datetime, timezone

from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository):

    async def find_by_hash(self, token_hash: str):
        return await self._collection.find_one({"token_hash": token_hash})

    async def revoke(self, token_id: str, replaced_by: str = None):
        await self._collection.update_one({"_id": ObjectId(token_id)},
                                          {"$set": {"revoked": True, "replaced_by": replaced_by}})

    async def delete_expired_revoked(self):
        await self._collection.delete_many({
            "revoke": True,
            "expires_at": {"$lt": datetime.now(timezone.utc)}
        })
