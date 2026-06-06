from datetime import datetime, timezone
from uuid import UUID, uuid7



class Role:
    def __init(self, role_name: str, description: str, _id: UUID = uuid7(), created_at: datetime | None = None):
        self.role_name = role_name
        self.description = description
        self._id = _id
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "role_name": self.role_name,
            "description": self.description,
            "created_at": self.created_at
        }