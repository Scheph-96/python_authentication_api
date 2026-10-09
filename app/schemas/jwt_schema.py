from datetime import datetime

from pydantic import BaseModel
from pydantic import field_validator


class JWTSchema(BaseModel):
    sub: str
    iss: str
    exp: datetime
    effective_permissions: list
    
    @field_validator("*")
    @classmethod
    def validate(cls, v):
        if v is not None and not v:
            if type(v) is not list:
                raise ValueError("Invalid Token")
        return v