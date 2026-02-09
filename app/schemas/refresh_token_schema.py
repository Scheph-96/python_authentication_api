from pydantic import BaseModel
from app.schemas.user_schema import BaseSchema

class RefreshTokenSchema(BaseSchema):
    refresh_token: str