from bson import ObjectId
from app.repositories.authentication_repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.authentication_repositories.user_repository import UserRepository
from app.core.config import Settings
from app.core.logging.logger import get_logger
from app.models.core_model.refresh_token_model import RefreshToken
from app.utils.jwt import hash_token
from fastapi import HTTPException
from datetime import datetime
import secrets

class RefreshTokenService:
    
    def __init__(self, refresh_token_repo: RefreshTokenRepository, user_repo: UserRepository):
        self.refresh_token_repo = refresh_token_repo
        self.user_repo = user_repo
        self.logger = get_logger("RefreshTokenService")
        
    async def create_refresh_token(self, user_id: str):
        raw = secrets.token_urlsafe(64)
        token_hash = hash_token(raw)
        
        user = await self.user_repo.find_by_id(user_id)
        
        refreshToken = RefreshToken(user_id=user_id, token_hash=token_hash, auth_version=user["auth_version"])
        
        refresh_token_id = await self.refresh_token_repo.create(refreshToken.to_dict())
        
        return {"raw_token": raw, "refresh_token_id": refresh_token_id}
    
    async def is_refresh_token_valid(self, token: str):
        token_hash = hash_token(token)
        
        record = await self.refresh_token_repo.find_by_hash(token_hash)
        
        # Invalid token when the token is revoked
        if not record or record["revoked"]:
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="TOKEN REVOKED"
            )
            raise HTTPException(401, "Invalid refresh token")
        
        refresh_token = RefreshToken(**record)
        
        # Timezone info of timezone aware variable
        my_timezone = refresh_token.expire_at.tzinfo
        # Current datetime for the timezone
        now = datetime.now(my_timezone)
        
        if refresh_token.expire_at < now:
            # Since the token has expired. We just revoke it
            await self.update_refresh_token(refresh_token._id)
            
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="TOKEN EXPIRED ==> REVOKE TOKEN"
            )
            
            raise HTTPException(401, "Invalid refresh token")
        
        user = await self.user_repo.find_by_id(str(refresh_token.user_id))
        
        if refresh_token.auth_version != user["auth_version"]:
            # Since the token version doesn't match. We just revoke it
            await self.update_refresh_token(refresh_token._id)
            
            self.logger.warning(
            Settings.SECURITY_EVENT_LABEL,
            detail="TOKEN VERSION INVALID ==> REVOKE TOKEN"
            )
            
            raise HTTPException(401, "Invalid refresh token")
        
        return refresh_token

    async def get_by_hash(self, token_hash: str):
        return await self.refresh_token_repo.find_by_hash(token_hash)
    
    async def update_refresh_token(self, token_id: ObjectId, replaced_by: str = None):
        await self.refresh_token_repo.revoke(str(token_id), replaced_by)
    
    async def delete_refresh_token(self):
        await self.refresh_token_repo.delete_expired_revoked()
        