from app.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository):

    async def find_by_name(self, permission_name: str):
        return await self.collection.find_one({"name": permission_name})