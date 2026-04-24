from app.core.logging.logger import get_logger
from app.repositories.authentication_repositories.user_repository import UserRepository


"""
    Here is our business logic
"""
class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self.logger = get_logger("UserService")

    async def create_user(self, data: dict):
        return await self._user_repository.create(data)
    
    async def get_by_id(self, user_id: str):
        return await self._user_repository.find_by_id(user_id)
    
    async def get_by_email(self, email: str):
        return await self._user_repository.find_by_email(email)
    
    async def get_by_username(self, username: str):
        return await self._user_repository.find_by_username(username)
    
    async def update_user(self, user_id: str, data: dict):
        await self._user_repository.update(user_id, data)

    async def update_users(self, user_ids: list, data: dict):
        await self._user_repository.update_many_user(user_ids, data)

    async def update_effective_permissions(self, updates: list):
        await self._user_repository.update_users_effective_permissions(updates)
    
    async def update_inc_user(self, user_id: str, data: dict):
        await self._user_repository.update_inc(user_id, data)