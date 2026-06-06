from datetime import datetime, timezone
from uuid import UUID, uuid7


class Permission:
    def __init(self, permission_name: str, _id: UUID = uuid7(), created_at: datetime | None = None):
        self.permission_name = permission_name
        self._id = _id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "permission_name": self.permission_name,
            "created_at": self.created_at
        }