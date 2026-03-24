from pydantic import field_validator

from app.schemas.base_schema import BaseSchema


class Base(BaseSchema):
    @field_validator("role_name", mode="after", check_fields=False)
    @classmethod
    def to_lower_case(cls, v: str):
        return v.lower()

class CreateRoleSchema(Base):
    description: str
    role_name: str

class AssignRoleSchema(BaseSchema):
    role_id: str
    user_id: str

class RemoveUserRoleSchema(AssignRoleSchema):
    pass

class DeleteRoleSchema(BaseSchema):
    role_id: str