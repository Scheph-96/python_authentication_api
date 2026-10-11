from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid7


class EmailValidationCode:
    def __init__(self,
                 user_id: str,
                 code_hash: str,
                 revoked: bool = False,
                 _id: UUID | None = None ,
                 expire_at: datetime | None = None,
                 created_at: datetime | None = None):
        self.user_id = UUID(user_id) if user_id is str else user_id
        self.code_hash = code_hash
        self.revoked = revoked
        self._id = _id or uuid7()
        self.expire_at = expire_at or datetime.now(timezone.utc) + timedelta(hours=1)
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "code_hash": self.code_hash,
            "revoked": self.revoked,
            "expire_at": self.expire_at,
            "created_at": self.created_at
        }
