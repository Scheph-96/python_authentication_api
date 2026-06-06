from datetime import datetime, timezone
from uuid import UUID, uuid7


class UserRole:
    def __init__(self, user_id: str, role_id: str, _id: UUID = uuid7(), created_at: datetime | None = None):
        self.user_id = user_id
        self.role_id = role_id
        self._id = _id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "created_at": self.created_at
        }