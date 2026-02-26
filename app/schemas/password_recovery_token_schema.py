from pydantic import BaseModel, EmailStr
from app.schemas.base_schema import BaseSchema


class PasswordRecoveryConfirmEmailSchema(BaseSchema):
    email: EmailStr
    
class PasswordRecoveryResetPasswordSchema(BaseSchema):
    token: str
    new_password: str