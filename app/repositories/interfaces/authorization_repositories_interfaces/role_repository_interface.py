from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class RoleRepositoryInterface(BaseRepositoryInterface):

    async def find_by_name(self, role_name: str):
        pass
