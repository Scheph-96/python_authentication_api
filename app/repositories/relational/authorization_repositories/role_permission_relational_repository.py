from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class RolePermissionRelationalRepository(BaseRelationalRepository, RolePermissionRepositoryInterface):
    async def find_by_role_id(self, role_id: str):
        pass

    async def find_by_role_ids(self, role_ids: list, options: dict = None):
        pass

    async def find_by_permission_id(self, permission_id: str):
        pass

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        pass

    async def delete_many_by_role_id(self, role_id: str):
        pass

    async def delete_many_by_permission_id(self, permission_id: str):
        pass
