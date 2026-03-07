from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository):

    async def find_by_name(self, role_name: str):
        return await self.collection.find_one({"name": role_name})
