from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.refresh_token_schema import RefreshTokenSchema
from app.core.config import Settings
from app.models.refresh_token_model import RefreshToken
from app.utils.jwt import create_access_token, hash_token
from fastapi import HTTPException
from datetime import datetime, timezone
import secrets

class RefreshTokenService:
    
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo
        
    async def create_refresh_token(self, user_id: str):
        raw = secrets.token_urlsafe(64)
        token_hash = hash_token(raw)
        refreshToken = RefreshToken(user_id= user_id, token_hash=token_hash)
        
        await self.repo.create(refreshToken.to_dict())
        
        return raw
    
    async def refresh(self, refresh_token: RefreshTokenSchema):
        token_hash = hash_token(refresh_token.refresh_token)
        
        record = await self.repo.find_by_hash(token_hash)
        
        # Invalid token when the token is revoked
        if not record or record["revoked"]:
            raise HTTPException(401, "Invalid refresh token")
        
        refresh_token = RefreshToken(**record)
        
        # Timezone info of timezone aware variable
        my_timezone = refresh_token.expire_at.tzinfo
        # Current datetime for the timezone
        now = datetime.now(my_timezone)
        
        if refresh_token.expire_at < now:
            
            raise HTTPException(401, "Refresh expired")
        
        user_id = str(refresh_token.user_id)
        
        # ROTATE
        # Generate new refresh token
        new_refresh = await self.create_refresh_token(user_id)
        
        new_hash = hash_token(new_refresh)
        
        # Revoke the old token
        await self.repo.revoke(refresh_token._id, new_hash)
        
        # Generate new access token
        new_access = create_access_token(user_id)
        
        return {"access_token":new_access, "refresh_token":new_refresh}
        
    
    async def get_by_hash(self, token_hash: str):
        return await self.repo.find_by_hash(token_hash)
    
    async def update_refresh_token(self, token_id: str, replaced_by: str):
        return await self.repo.revoke(token_id, replaced_by)
    
    async def delete_refresh_token(self):
        return await self.repo.delete_expired_revoked()
        