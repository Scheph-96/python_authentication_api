from app.schemas.base_schema import BaseSchema


class AssignRoleSchema(BaseSchema):
    role_id: str
    user_id: str