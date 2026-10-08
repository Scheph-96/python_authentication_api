from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface

class UserRepositoryInterface(BaseRepositoryInterface):

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

