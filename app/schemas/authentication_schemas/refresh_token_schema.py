from pydantic import BaseModel
from app.schemas.base_schema import BaseSchema


class RefreshTokenSchema(BaseSchema):
    refresh_token: str