from app.repositories.interfaces.authorization_repositories.user_role_repository_interface import \
    UserRoleRepositoryInterface


class RelationalUserRoleRepository(UserRoleRepositoryInterface):
    async def find_by_role_id(self, role_id: str, options: dict = None):
        return await super().find_by_role_id(role_id, options)

    async def find_by_user_id(self, user_id: str, options: dict = None):
        return await super().find_by_user_id(user_id, options)

    async def find_by_user_ids(self, user_ids: list, options: dict = None):
        return await super().find_by_user_ids(user_ids, options)

    async def delete_many_by_role_id(self, role_id: str):
        return await super().delete_many_by_role_id(role_id)

    async def get_user_ids_by_role_id(self, role_id: str):
        return await super().get_user_ids_by_role_id(role_id)

    async def get_users_and_permissions(self, user_ids: list):
        return await super().get_users_and_permissions(user_ids)