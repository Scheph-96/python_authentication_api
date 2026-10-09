from app.repositories.interfaces.authorization_repositories.role_permission_repository_interface import \
    RolePermissionRepositoryInterface


class RelationalRolePermissionRepository(RolePermissionRepositoryInterface):
    async def find_by_role_id(self, role_id: str):
        return await super().find_by_role_id(role_id)

    async def find_by_role_ids(self, role_ids: list, options: dict = None):
        return await super().find_by_role_ids(role_ids, options)

    async def find_by_permission_id(self, permission_id: str):
        return await super().find_by_permission_id(permission_id)

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        return await super().get_user_ids_from_role_permissions(permission_id)

    async def delete_many_by_role_id(self, role_id: str):
        return await super().delete_many_by_role_id(role_id)

    async def delete_many_by_permission_id(self, permission_id: str):
        return await super().delete_many_by_permission_id(permission_id)