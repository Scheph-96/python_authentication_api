from app.repositories.interfaces.authentication_repositories.user_repository_interface import UserRepositoryInterface


class RelationalUserRepository(UserRepositoryInterface):

    async def find_by_email(self, email: str):
        pass

    async def find_by_username(self, username: str):
        pass

    async def update_inc(self, user_id: str, data: dict):
        pass

    async def update_many_user(self, user_ids: list, data: dict):
        pass

    async def update_users_effective_permissions(self, updates: list):
        pass

