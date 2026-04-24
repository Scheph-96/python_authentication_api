from app.repositories.authorization_repositories.role_permission_repository import RolePermissionRepository


class RolePermissionService:
    def __init__(self, role_permission_repository: RolePermissionRepository):
        self._role_permission_repository = role_permission_repository

    async def create_role_permission(self, data: dict):
        return await self._role_permission_repository.create(data)

    async def create_role_permissions(self, data: list):
        return await self._role_permission_repository.create_many(data)

    async def find_all_role_permissions(self, options: dict = None):
        return await self._role_permission_repository.find_all(options)

    async def find_role_permission(self, data: dict, options: dict = None):
        return await self._role_permission_repository.find(data, options=options)

    async def find_role_permission_by_id(self, role_permission_id: str):
        return await self._role_permission_repository.find_by_id(role_permission_id)

    async def find_role_permission_by_role_id(self, role_id: str) -> list:
        return await self._role_permission_repository.find_by_role_id(role_id)

    async def find_role_permission_by_role_ids(self, role_ids: list, options: dict = None) -> list:
        return await self._role_permission_repository.find_by_role_ids(role_ids)

    async def find_role_permission_by_permission_id(self, permission_id: str) -> list:
        return await self._role_permission_repository.find_by_permission_id(permission_id)

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        return await self._role_permission_repository.get_user_ids_from_role_permissions(permission_id)

    async def update_role_permission(self, role_permission_id: str, data: dict):
        await self._role_permission_repository.update(role_permission_id, data)

    async def delete_one_role_permission(self, role_permission: dict):
        await self._role_permission_repository.delete(role_permission)

    async def delete_one_role_permission_by_id(self, role_permission_id: str):
        await self._role_permission_repository.delete_one(role_permission_id)

    async def delete_many_role_permissions_by_role_id(self, role_id: str):
        await self._role_permission_repository.delete_many_by_role_id(role_id)

    async def delete_many_role_permissions_by_permission_id(self, permission_id: str):
        await self._role_permission_repository.delete_many_by_permission_id(permission_id)