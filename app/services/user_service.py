from app.repositories.user_repository import UserRepository
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.schemas.email_validation_code import EmailValidationCode
from app.utils.resources import code_generator
from app.utils.jwt import hash_token
from app.utils.email import send_email, verification_email_template
from fastapi import HTTPException, BackgroundTasks


"""
    Here is our business logic
"""
class UserService:
    def __init__(self, repo: UserRepository, base_repo: BaseRepository):
        self.repo = repo
        self.base_repo = base_repo
        
    """
        Create an account for the user
    """
    async def create_user(self, data: dict, background_tasks: BackgroundTasks):
        
        if await self.repo.find_by_email(data["email"]):
            raise HTTPException(400, "Email already exist")
        
        if await self.repo.find_by_username(data["username"]):
            raise HTTPException(400, "Username already exist")
        
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        
        user_id = await self.repo.create(user.to_dict())
        
        code = code_generator()
        email_validation_code = EmailValidationCode(user_id=user_id, code_hash=hash_token(code))
        
        await self.base_repo.create(email_validation_code.model_dump())
        
        html = verification_email_template(code)
        
        background_tasks.add_task(send_email, user.email, "Email Validation", html) 
        
        return user_id
    
    async def get_by_email(self, email: str):
        return await self.repo.find_by_email(email)
    
    async def get_by_username(self, username: str):
        return await self.repo.find_by_username(username)
    
    async def update_user(self, user_id: str, data: dict):
        await self.repo.update(user_id, data)