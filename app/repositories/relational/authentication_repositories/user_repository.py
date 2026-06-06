from bson import ObjectId
from pymongo import UpdateOne

from app.repositories.document.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def find_by_email(self, email: str):
        return await self._collection.find_one({"email": email})

    async def find_by_username(self, username: str):
        return await self._collection.find_one({"username": username})

    async def update_inc(self, user_id: str, data: dict):
        await self._collection.update_one({"_id": ObjectId(user_id)}, {"$inc": data})

    async def update_many_user(self, user_ids: list, data: dict):
        await self._collection.update_many({"_id": {"$in": user_ids}}, {"$set": data})

    async def update_users_effective_permissions(self, updates: list):

        operations = [
            UpdateOne(
                {"_id": item["user_id"]},
                {"$set": {
                    "effective_permissions": item["permissions"]
                    }
                }
            )
            for item in updates
        ]

        await self._collection.bulk_write(operations)

