from pydantic import EmailStr, model_validator
from typing import Optional

from app.schemas.base_schema import BaseSchema

class UserSignUpSchema(BaseSchema):
    username: str
    email: EmailStr
    password: str
    
class UserSignInSchema(BaseSchema):
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
    
class UserLogOutSchema(BaseSchema):
    refresh_token: str
    