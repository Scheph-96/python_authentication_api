from app.repositories.interfaces.authorization_repositories_interfaces.role_repository_interface import \
    RoleRepositoryInterface
from app.repositories.relational.base_relational_repository import BaseRelationalRepository


class RoleRepository(BaseRelationalRepository, RoleRepositoryInterface):
    async def find_by_name(self, role_name: str):
        pass
