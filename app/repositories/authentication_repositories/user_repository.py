from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def find_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def find_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def update_inc(self, user_id: str, data: dict):
        await self.collection.update_one({"_id": ObjectId(user_id)}, {"$inc": data})
