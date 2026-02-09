from pydantic import BaseModel, EmailStr
from app.schemas.user_schema import BaseSchema

class PasswordRecoveryConfirmEmailSchema(BaseSchema):
    email: EmailStr
    
class PasswordRecoveryResetPasswordSchema(BaseSchema):
    token: str
    password: str