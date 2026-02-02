from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta

class EmailValidationCode(BaseModel):
    user_id: str
    code_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expire_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    
class EmailValidationCodeSubmit(BaseModel):
    user_id: str
    code: str