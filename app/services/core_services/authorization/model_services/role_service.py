from app.repositories.document.authorization_repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def create_role(self, data: dict):
        return await self.role_repository.create(data)
    
    async def find_role_by_id(self, role_id: str):
        return await self.role_repository.find_by_id(role_id)

    async def find_role_by_name(self, role_name: str):
        return await self.role_repository.find_by_name(role_name)

    async def update_role(self, role_id: str, updated_data: dict):
        await self.role_repository.update(role_id, updated_data)

    async def delete_role(self, role_id: str):
        await self.role_repository.delete_one(role_id)
