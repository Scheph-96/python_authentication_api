from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
from app.schemas.user_schema import BaseSchema

class EmailValidationCode(BaseSchema):
    user_id: str
    code_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expire_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=1))
    
class EmailValidationCodeSubmit(BaseSchema):
    user_id: str
    code: str
    
class EmailValidationCodeRetry(BaseSchema):
    user_id: str