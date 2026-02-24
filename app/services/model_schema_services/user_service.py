from app.core.logging.logger import get_logger
from app.repositories.user_repository import UserRepository


"""
    Here is our business logic
"""
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.logger = get_logger("UserService")

    async def create_user(self, data: dict):
        return await self.repo.create(data)
    
    async def get_by_id(self, user_id: str):
        return await self.repo.find_by_id(user_id)
    
    async def get_by_email(self, email: str):
        return await self.repo.find_by_email(email)
    
    async def get_by_username(self, username: str):
        return await self.repo.find_by_username(username)
    
    async def update_user(self, user_id: str, data: dict):
        await self.repo.update(user_id, data)
    
    async def update_inc_user(self, user_id: str, data: dict):
        await self.repo.update_inc(user_id, data)