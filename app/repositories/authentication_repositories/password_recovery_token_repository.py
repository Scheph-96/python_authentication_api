from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class PasswordRecoveryTokenRepository(BaseRepository):

    async def find_by_hash(self, token_hash: str):
        return await self._collection.find_one({"token_hash": token_hash})

    async def find_by_user_id(self, user_id: str):
        return await self._collection.find_one({"user_id": ObjectId(user_id)})

    async def invalidate_token(self, recovery_token_id: str):
        await self._collection.update_one({"_id": ObjectId(recovery_token_id)}, {"$set": {"is_used": True}})
