from datetime import datetime, timezone

from argon2 import PasswordHasher
from bson import ObjectId

"""
    The user model
"""

passwordHash = PasswordHasher()


class User:
    def __init__(
            self,
            username: str,
            email: str,
            auth_version: int = 0,
            _id: ObjectId = None,
            hashed_password: str | None = None,
            effective_permissions: list = None,
            is_verified: bool = False,
            created_at: datetime | None = None):
        self.username = username
        self.email = email
        self.auth_version = auth_version
        self._id = _id
        self.hashed_password = hashed_password
        self.effective_permissions = effective_permissions
        self.is_verified = is_verified
        self.created_at = created_at or datetime.now(timezone.utc)

    # -------- Domain Behavior --------

    def set_password(self, raw_password: str) -> None:
        self.hashed_password = passwordHash.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return passwordHash.verify(self.hashed_password, raw_password)

    def add_effective_permissions(self, permission: str) -> None:
        self.effective_permissions.append(permission)

    def remove_effective_permissions(self, permission: str) -> None:
        self.effective_permissions.remove(permission)

    # -------- Serialization --------

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "auth_version": self.auth_version,
            "hashed_password": self.hashed_password,
            "effective_permissions": self.effective_permissions,
            "is_verified": self.is_verified,
            "created_at": self.created_at
        }
