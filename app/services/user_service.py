from app.repositories.user_repository import UserRepository
from fastapi import HTTPException
from app.models.user_model import User


"""
    Here is our business logic

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
"""
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    """
        Create an account for the user
    """
    async def create_user(self, data: dict):
        if await self.repo.find_by_email(data["email"]):
            raise HTTPException(400, "Email already exist")
        
        if await self.repo.find_by_username(data["username"]):
            raise HTTPException(400, "Username already exist")
        
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        
        return await self.repo.create(user.to_dict())
    
    async def get_by_email(self, email: str):
        return await self.repo.find_by_email(email)
    
    async def get_by_username(self, username: str):
        return await self.repo.find_by_username(username)