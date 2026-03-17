from app.repositories.authorization_repositories.permission_repository import PermissionRepository


class PermissionService:
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def create_permission(self, data: dict):
        return await self.permission_repository.create(data)

    async def find_permission_by_id(self, permission_id: str, options: dict = None):
        return await self.permission_repository.find_by_id(permission_id, options)

    async def find_permission_by_ids(self, permission_ids: list, options: dict = None)-> list:
        return await self.permission_repository.find_by_ids(permission_ids, options)

    async def find_permission_by_name(self, permission_name: str, options: dict = None):
        return await self.permission_repository.find_by_name(permission_name, options)

    async def update_permission(self, permission_id: str, updated_data: dict):
        await self.permission_repository.update(permission_id, updated_data)

    async def delete_permission(self, permission_id: str):
        await self.permission_repository.delete(permission_id)