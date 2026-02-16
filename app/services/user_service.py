from app.core.logging.logger import get_logger
from app.core.config import Settings
from app.repositories.user_repository import UserRepository
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.schemas.email_validation_code import EmailValidationCode
from app.utils.resources import code_generator
from app.utils.jwt import hash_token
from app.utils.email import email_processing
from fastapi import HTTPException, BackgroundTasks


"""
    Here is our business logic
"""
class UserService:
    def __init__(self, repo: UserRepository, email_validation_repository: BaseRepository):
        self.repo = repo
        self.email_validation_repository = email_validation_repository
        self.logger = get_logger("UserService")
        
    """
        Create an account for the user
    """
    async def user_registration(self, data: dict, background_tasks: BackgroundTasks):
        
        # One email per user, no duplication
        if await self.repo.find_by_email(data["email"]):
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail=f"EMAIL {data["email"]} ALREADY EXIST"
            )
            
            raise HTTPException(400, "Invalid Credential")
        
        # Unique username
        if await self.repo.find_by_username(data["username"]):
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail=f"USERNAME {data["username"]} ALREADY EXIST"
            )
            
            raise HTTPException(400, "Invalid Credential")
        
        user = User(username=data["username"], email=data["email"])
        
        # This method hash the password
        user.set_password(data["password"])
        
        # Create user and get the id
        user_id = await self.repo.create(user.to_dict())
        user._id = user_id
        
        # Send email to validate the user email address in background
        background_tasks.add_task(email_processing, user, self.email_validation_repository)
        
        self.logger.info(
        Settings.SECURITY_EVENT_LABEL,
        detail=f"USER CREATED SUCCESSFULLY",
        user_id=str(user._id)
        )
        
        # retrieve user id
        return user._id
    
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