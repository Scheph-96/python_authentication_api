import unicodedata
from pydantic import BaseModel, EmailStr, model_validator, field_validator
from typing import Optional

class BaseSchema(BaseModel):
    """
        Common sanitization for all schemas.
    """
    
    @field_validator("*", mode="before")
    @classmethod
    def sanitize_strings(cls, v):
        if not isinstance(v, str):
            return v
        
        # Unicode normalization (security + consistency)
        v = unicodedata.normalize("NFKC", v)
        
        # Remove invisible characters (zero-width space)
        v = v.replace("\u200b", "")
        
        # Normalize line endings
        v = v.replace("\r\n", "\n")
        
        # Trim whitespace
        return v.strip()
    
    model_config = {
        "extra": "forbid", # reject unknown fields
        "str_strip_whitespace": False, # we control trimming ourselves
    }

class UserCreateSchema(BaseSchema):
    username: str
    email: EmailStr
    password: str
    
    # Reject empty strings. "" or " "
    @field_validator("username", "email")
    @classmethod
    def validate(cls, v):
        if v is not None and not v:
            raise ValueError("Field cannot be empty")
        return v
    
class UserGetSchema(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    
    """
        We want to authenticate the user whether with his username or his email
    """
    @model_validator(mode='before')
    def check_username_or_email(cls, values):
        username = values.get("username")
        email = values.get("email")
        
        if not username and not email:
            raise ValueError("username or email is required")
        
        return values
    
class UserResponseSchema(BaseModel):
    _id: str
    username: str
    email: str