from app.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository):

    async def find_by_name(self, permission_name: str, options: dict = None):
        return await self._collection.find_one({"name": permission_name}, options)

    async def find_by_ids(self, permission_ids: list, options: dict = None):
        result = self._collection.find({"_id": {"$in": permission_ids}}, options)
        return await result.to_list()