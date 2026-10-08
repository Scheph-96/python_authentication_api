from app.repositories.interfaces.authorization_repositories_interfaces.permission_repository_interface import \
    PermissionRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class PermissionRelationalRepository(BaseRelationalRepository, PermissionRepositoryInterface):
    async def find_by_name(self, permission_name: str, options: dict = None):
        pass

    async def find_by_name_in(self, permissions_names: list, options: dict = None):
        pass

    async def find_by_ids(self, permission_ids: list, options: dict = None):
        pass
