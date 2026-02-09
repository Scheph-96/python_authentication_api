from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone, timedelta

class PasswordRecoveryConfirmEmailSchema(BaseModel):
    email: EmailStr
    
class PasswordRecoveryUpdatePasswordSchema(BaseModel):
    token: str
    password: str