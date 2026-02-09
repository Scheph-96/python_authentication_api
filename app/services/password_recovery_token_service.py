from datetime import datetime, timezone
from app.models.password_recovery_token_model import PasswordRecoveryToken
from app.repositories.password_recovery_token_repository import PasswordRecoveryTokenRepository
from app.utils.jwt import hash_token
import secrets

class PasswordRecoveryTokenService:
    
    def __init__(self, repo: PasswordRecoveryTokenRepository):
        self.repo = repo
        
    async def create_password_recovery_token(self, user_id: str):
        # Generate the recovery token
        raw_token = secrets.token_urlsafe(32)
        # Hash the token
        token_hash = hash_token(raw_token)
        
        # Create the schema
        password_recovery_token = PasswordRecoveryToken(user_id=str(user_id), token_hash=token_hash)
        await self.repo.create(password_recovery_token.to_dict())
        
        return  raw_token
    
    async def get_by_hash(self, token_hash: str):
        return await self.repo.find_by_hash(token_hash)
    
    async def get_by_user_id(self, user_id: str):
        return await self.repo.find_by_user_id(user_id)
    
    async def invalidate_password_recovery_token(self, password_recovery_instance_id: str):        
        await self.repo.invalidate_token(password_recovery_instance_id)
        
    async def delete_password_recovery_token(self, recovery_token_id):
        await self.repo.delete(recovery_token_id)