from datetime import datetime, timezone, timedelta
from bson import ObjectId

class PasswordRecoveryToken:
    
    def __init__(self, user_id: str, token_hash: str, used: bool = False, expire_at: datetime | None = None, created_at: datetime | None = None):
        self.user_id = ObjectId(user_id)
        self.token_hash = token_hash
        self.expire_at = expire_at or datetime.now(timezone.utc) + timedelta(minutes=30)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.used = used
        
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "token_hash": self.token_hash,
            "expire_at": self.expire_at,
            "created_at": self.created_at,
            "used": self.used
        }