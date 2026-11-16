from uuid import UUID

from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface


class UserRoleRepositoryInterface(BaseRepositoryInterface):

    async def find_by_role_id(self, role_id: UUID, **kwargs):
        pass

    async def find_by_user_id(self, user_id: UUID, **kwargs):
        pass

    async def find_by_user_ids(self, user_ids: list, **kwargs):
        pass

    async def delete_many_by_role_id(self, role_id: UUID):
        pass

    async def get_user_ids_by_role_id(self, role_id: UUID):
        pass

    async def get_users_and_permissions(self, user_ids: list):
        pass
