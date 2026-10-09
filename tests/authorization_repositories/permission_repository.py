from app.repositories.interfaces.authorization_repositories.permission_repository_interface import \
    PermissionRepositoryInterface


class RelationalPermissionRepository(PermissionRepositoryInterface):

    async def find_by_name(self, permission_name: str, options: dict = None):
        return await super().find_by_name(permission_name, options)

    async def find_by_name_in(self, permissions_names: list, options: dict = None):
        return await super().find_by_name_in(permissions_names, options)

    async def find_by_ids(self, permission_ids: list, options: dict = None):
        return await super().find_by_ids(permission_ids, options)