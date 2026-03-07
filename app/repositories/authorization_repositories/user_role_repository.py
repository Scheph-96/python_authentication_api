from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class UserRoleRepository(BaseRepository):

    def find_by_role_id(self, role_id: str):
        return self.collection.find({"role_id": ObjectId(role_id)})

    def find_by_user_id(self, user_id: str):
        return self.collection.find({"user_id": ObjectId(user_id)})
