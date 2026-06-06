from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid7

from app.core.config import settings


class RefreshToken:

    def __init__(self, user_id: str, token_hash: str, auth_version: int, replaced_by: str = None, revoked: bool = False,
                 _id: UUID = uuid7(), expire_at: datetime | None = None, created_at: datetime | None = None):
        self.user_id = UUID(user_id)
        self.token_hash = token_hash
        self.auth_version = auth_version  # The authentication/token version of the user model
        self.replaced_by = replaced_by  # if this refresh token was used, which new token replaced it ?
        self.revoked = revoked
        self._id = _id
        self.expire_at = expire_at or datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRATION_DAYS)
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "token_hash": self.token_hash,
            "auth_version": self.auth_version,
            "replaced_by": self.replaced_by,
            "revoked": self.revoked,
            "expire_at": self.expire_at,
            "created_at": self.created_at
        }
