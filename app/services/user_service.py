from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponseSchema
from fastapi import HTTPException

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
        # Check if a user with the provided email already exist
        if await self.repo.find_by_email(data["email"]):
            raise HTTPException(400, "Email already exit")
        
        # Check if a user with the provided username already exist
        if await self.repo.find_by_username(data["username"]):
            raise HTTPException(400, "Username already exist")
        
        return await self.repo.create(data)
    
    """
        Authenticate a user
        
        We want to log our users in whether with the 
        email or the username
    """
    async def get_user(self, data: dict):
        # If the request body provide a username attribute then the login is performed with the username
        if data.get("username"):
            user = await self.repo.find_by_username(data["username"])
            return UserResponseSchema(**user)
        
        # If the request body provide a email attribute then the login is performed with the email
        elif data.get("email"):
            user = await self.repo.find_by_email(data["email"])
            return UserResponseSchema(**user)
        
        else:
            raise HTTPException(422, "Missing 'username' or 'email'")