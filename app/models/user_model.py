
from passlib.content import CryptContext
from datetime import datetime

"""
    The user model
"""
class User:
    def __init__(self, username: str, email: str, hashed_password: str | None = None, created_at: datetime | None = None):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.timezone.utc()
        
    # -------- Domain Behavior --------
    
    def set_password(self, raw_password: str) -> None:
        self.hashed_password = pwd_context.hash(raw_password)
        
    def verify_password(self, raw_password: str) -> bool:
        return pwd_context.verify(raw_password, self.hashed_password)
    
    # -------- Serialization --------
    
    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
    