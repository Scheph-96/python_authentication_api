from pydantic import field_validator

from app.schemas.base_schema import BaseSchema


class Base(BaseSchema):
    @field_validator("permissions_names", mode="after", check_fields=False)
    @classmethod
    def to_lower_case(cls, v: list):
        return [str(item).lower() for item in v]


class CreatePermissionSchema(Base):
    permission_name: str


class AssignPermissionToRoleSchema(BaseSchema):
    role_id: str
    permission_id: str

class RemovePermissionFromRoleSchema(AssignPermissionToRoleSchema):
    pass


class DeletePermissionSchema(BaseSchema):
    pass
