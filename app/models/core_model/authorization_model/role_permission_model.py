from datetime import datetime, timezone
from uuid import UUID, uuid7


class RolePermission:
    def __init__(self, role_id: str, permission_id: str, _id: UUID = uuid7(), created_at: datetime | None = None):
        self.role_id = role_id
        self.permission_id = permission_id
        self._id = _id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "_id": self._id,
            "role_id": self.role_id,
            "permission_id": self.permission_id,
            "created_at": self.created_at
        }