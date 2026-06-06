from app.repositories.document.authorization_repositories.permission_repository import PermissionRepository
from app.utils.resources import string_list_to_objectid


class PermissionService:
    def __init__(self, permission_repository: PermissionRepository):
        self._permission_repository = permission_repository

    async def create_permission(self, data: dict) -> str:
        return await self._permission_repository.create(data)

    async def create_permissions(self, data: list) -> list:
        return await self._permission_repository.create_many(data)

    async def find_permission_by_id(self, permission_id: str, options: dict = None):
        return await self._permission_repository.find_by_id(permission_id, options)

    async def find_permission_by_ids(self, permission_ids: list, options: dict = None)-> list:
        return await self._permission_repository.find_by_ids(permission_ids, options)

    async def find_permission_by_name(self, permission_name: str, options: dict = None):
        return await self._permission_repository.find_by_name(permission_name, options)

    async def find_permission_by_name_in(self, permissions_names: list, options: dict = None):
        return await self._permission_repository.find_by_name_in(permissions_names, options)

    async def update_permission(self, permission_id: str, updated_data: dict):
        await self._permission_repository.update(permission_id, updated_data)

    async def delete_permission(self, permission_id: str):
        await self._permission_repository.delete_one(permission_id)

    async def delete_permissions_in(self, permissions_ids: list):
        await self._permission_repository.delete_many_in(string_list_to_objectid(permissions_ids))