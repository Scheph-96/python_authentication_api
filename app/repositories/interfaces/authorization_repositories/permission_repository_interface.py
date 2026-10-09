class PermissionRepositoryInterface:

    async def find_by_name(self, permission_name: str, options: dict = None):
        pass

    async def find_by_name_in(self, permissions_names: list, options: dict = None):
        pass

    async def find_by_ids(self, permission_ids: list, options: dict = None):
        pass
