from uuid import UUID

from app.repositories.document.authorization_repositories.role_permission_document_repository import RolePermissionDocumentRepository
from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface
from app.utils.resources import dict_string_to_uuid


class RolePermissionService:
    def __init__(self, role_permission_repository: RolePermissionRepositoryInterface):
        self._role_permission_repository = role_permission_repository

    async def create_role_permission(self, data: dict):
        return await self._role_permission_repository.create(dict_string_to_uuid(data))

    async def create_role_permissions(self, data: list):
        return await self._role_permission_repository.create_many(data)

    async def find_all_role_permissions(self, options: dict | None = None):
        return await self._role_permission_repository.find_all(options=options)

    async def find_role_permission(self, data: dict, options: dict | None = None):
        return await self._role_permission_repository.find(dict_string_to_uuid(data), options=options)

    async def find_role_permission_by_id(self, role_permission_id: str):
        return await self._role_permission_repository.find_by_id(role_permission_id)

    async def find_role_permission_by_role_id(self, role_id: str) -> list:
        return await self._role_permission_repository.find_by_role_id(UUID(role_id))

    async def find_role_permission_by_role_ids(self, role_ids: list, options: dict | None = None) -> list:
        return await self._role_permission_repository.find_by_role_ids(role_ids, options=options)

    async def find_role_permission_by_permission_id(self, permission_id: str) -> list:
        return await self._role_permission_repository.find_by_permission_id(UUID(permission_id))

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        return await self._role_permission_repository.get_user_ids_from_role_permissions(UUID(permission_id))

    async def update_role_permission(self, role_permission_id: str, data: dict):
        await self._role_permission_repository.update(role_permission_id, data)

    async def delete_one_role_permission(self, role_permission: dict):
        await self._role_permission_repository.delete(role_permission)

    async def delete_one_role_permission_by_id(self, role_permission_id: str):
        await self._role_permission_repository.delete_one_by_id(role_permission_id)

    async def delete_many_role_permissions_by_role_id(self, role_id: str):
        await self._role_permission_repository.delete_many_by_role_id(UUID(role_id))

    async def delete_many_role_permissions_by_permission_id(self, permission_id: str):
        await self._role_permission_repository.delete_many_by_permission_id(UUID(permission_id))