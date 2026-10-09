from app.repositories.interfaces.authorization_repositories.role_repository_interface import RoleRepositoryInterface


class RelationalRoleRepository(RoleRepositoryInterface):

    async def find_by_name(self, role_name: str):
        return await super().find_by_name(role_name)