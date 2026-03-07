from app.repositories.authorization_repositories.permission_repository import PermissionRepository


class PermissionService:
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def create_permission(self, data: dict):
        return await self.permission_repository.create(data)

    async def find_permission_by_id(self, permission_id: str):
        return await self.permission_repository.find_by_id(permission_id)

    async def find_permission_by_name(self, permission_name: str):
        return await self.permission_repository.find_by_name(permission_name)

    async def update_permission(self, permission_id: str, updated_data: dict):
        await self.permission_repository.update(permission_id, updated_data)

    async def delete_permission(self, permission_id: str):
        await self.permission_repository.delete(permission_id)