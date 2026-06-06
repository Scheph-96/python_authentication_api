from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid7

from app.core.config import Settings


class PasswordRecoveryToken:

    def __init__(self, user_id: str, token_hash: str, is_used: bool = False, _id: UUID = uuid7(),
                 expire_at: datetime | None = None, created_at: datetime | None = None):
        self.user_id = UUID(user_id)
        self.token_hash = token_hash
        self._id = _id
        self.expire_at = expire_at or datetime.now(timezone.utc) + timedelta(
            minutes=Settings.PASSWORD_RECOVERY_TOKEN_EXPIRATION_MINUTES)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.is_used = is_used

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "token_hash": self.token_hash,
            "expire_at": self.expire_at,
            "created_at": self.created_at,
            "is_used": self.is_used
        }
