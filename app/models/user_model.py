from datetime import datetime, timezone
from argon2 import PasswordHasher
from bson import ObjectId

"""
    The user model
"""

passwordHash = PasswordHasher()

class User:
    def __init__(self,username: str, email: str,  _id: ObjectId = None, hashed_password: str | None = None, created_at: datetime | None = None):
        self.username = username
        self.email = email
        self._id = _id
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.now(timezone.utc)
        
    # -------- Domain Behavior --------
    
    def set_password(self, raw_password: str) -> None:
        self.hashed_password = passwordHash.hash(raw_password)
        
    def verify_password(self, raw_password: str) -> bool:
        return passwordHash.verify(self.hashed_password, raw_password)
    
    # -------- Serialization --------
    
    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
    