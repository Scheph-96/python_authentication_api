from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class UserRoleRepository(BaseRepository):

    async def find_by_role_id(self, role_id: str):
        result = self.collection.find({"role_id": ObjectId(role_id)})
        return await result.to_list()

    async def find_by_user_id(self, user_id: str, options: dict = None):
        result = self.collection.find({"user_id": ObjectId(user_id)}, options)
        return await result.to_list()
