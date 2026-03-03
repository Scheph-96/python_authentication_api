from datetime import datetime, timedelta, timezone

from bson import ObjectId


class EmailValidationCode:
    def __init__(self, user_id: str, code_hash: str, is_used: bool = False, _id: ObjectId = None,
                 expire_at: datetime | None = None, created_at: datetime | None = None):
        self.user_id = ObjectId(user_id)
        self.code_hash = code_hash
        self.is_used = is_used
        self._id = _id
        self.expire_at = expire_at or datetime.now(timezone.utc) + timedelta(hours=1)
        self.created_at= created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "code_hash": self.code_hash,
            "is_used": self.is_used,
            "expire_at": self.expire_at,
            "created_at": self.created_at
        }
