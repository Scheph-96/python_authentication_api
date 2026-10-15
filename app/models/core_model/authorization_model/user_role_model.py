from datetime import datetime, timezone
from uuid import UUID, uuid7


class UserRole:
    def __init__(self,
                 user_id: str,
                 role_id: str,
                 _id: UUID | None = None,
                 created_at: datetime | None = None):
        self.user_id = UUID(user_id) if type(user_id) is str else user_id
        self.role_id = UUID(role_id) if type(role_id) is str else role_id
        self._id = _id or uuid7()
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "created_at": self.created_at
        }