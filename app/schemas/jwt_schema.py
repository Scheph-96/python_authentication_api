from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException, status
from pydantic import field_validator

class JWTSchema(BaseModel):
    sub: str
    iss: str
    exp: datetime
    
    @field_validator("*")
    @classmethod
    def validate(cls, v):
        if v is not None and not v:
            raise ValueError("Invalid Token")
        return v