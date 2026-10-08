from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class UserRoleRepositoryInterface(BaseRepositoryInterface):

    async def find_by_role_id(self, role_id: str, options: dict = None):
        pass

    async def find_by_user_id(self, role_id: str, options: dict = None):
        pass

    async def find_by_user_ids(self, user_ids: list, options: dict = None):
        pass

    async def delete_many_by_role_id(self, role_id: str):
        pass

    async def get_user_ids_by_role_id(self, role_id: str):
        pass

    async def get_users_and_permissions(self, user_ids: list):
        pass
