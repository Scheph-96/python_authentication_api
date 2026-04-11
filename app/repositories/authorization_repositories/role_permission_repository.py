from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class RolePermissionRepository(BaseRepository):
    
    async def find_by_role_id(self, role_id: str):
        result = self._collection.find({"role_id": ObjectId(role_id)})
        return await result.to_list()

    async def find_by_role_ids(self, role_ids: list, options: dict = None):
        result = self._collection.find({"role_id": {"$in": role_ids}}, options)
        return await result.to_list()
    
    async def find_by_permission_id(self, permission_id: str):
        result = self._collection.find({"permission_id": ObjectId(permission_id)})
        return await result.to_list()

    async def delete_many_by_role_id(self, role_id: str):
        await self._collection.delete_many({"role_id": ObjectId(role_id)})

    async def delete_many_by_permission_id(self, permission_id: str):
        await self._collection.delete_many({"permission_id": ObjectId(permission_id)})