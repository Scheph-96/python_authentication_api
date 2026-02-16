from datetime import datetime
from app.models.password_recovery_token_model import PasswordRecoveryToken
from app.schemas.password_recovery_token_schema import PasswordRecoveryResetPasswordSchema
from app.repositories.password_recovery_token_repository import PasswordRecoveryTokenRepository
from app.utils.jwt import hash_token
from fastapi import HTTPException
import secrets

class PasswordRecoveryTokenService:
    
    def __init__(self, repo: PasswordRecoveryTokenRepository):
        self.repo = repo
        
    async def create_password_recovery_token(self, user_id: str):
        # Generate the recovery token
        raw_token = secrets.token_urlsafe(32)
        # Hash the token
        token_hash = hash_token(raw_token)
        
        # Create the model
        password_recovery_token = PasswordRecoveryToken(user_id=str(user_id), token_hash=token_hash)
        password_recovery_token_id = await self.repo.create(password_recovery_token.to_dict())
        
        return  {"raw_token": raw_token, "password_recovery_token_id": password_recovery_token_id}
    
    async def invalidate_token(self, token: str):
        token_hash = hash_token(token)
        
        password_recovery_token = await self.repo.find_by_hash(token_hash)
        
        if not password_recovery_token:
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="PASSWORD RECOVERY TOKEN NOT FOUND"
            )
            
            raise HTTPException(401, "Invalid Token")
        
        password_recovery_token = PasswordRecoveryToken(**password_recovery_token)
        
        # Timezone info of timezone aware variable
        my_timezone = password_recovery_token.expire_at.tzinfo
        # Current datetime for the timezone
        now = datetime.now(my_timezone)
        
        # Check token expiration
        if password_recovery_token.expire_at < now:
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="PASSWORD RECOVERY TOKEN EXPIRED"
            )
            
            raise HTTPException(401, "Invalid Token")
        
        # Check whether was used or not
        if password_recovery_token.used:
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="PASSWORD RECOVERY TOKEN USED"
            )
            
            raise HTTPException(401, "Invalid Token")
        
        await self.repo.invalidate_token(password_recovery_token._id)
        
        return password_recovery_token.user_id
        
    
    async def get_by_hash(self, token_hash: str):
        return await self.repo.find_by_hash(token_hash)
    
    async def get_by_user_id(self, user_id: str):
        return await self.repo.find_by_user_id(user_id)
    
    async def update_password_recovery_token(self, password_recovery_instance_id: str):        
        await self.repo.invalidate_token(password_recovery_instance_id)
        
    async def delete_password_recovery_token(self, recovery_token_id):
        await self.repo.delete(recovery_token_id)