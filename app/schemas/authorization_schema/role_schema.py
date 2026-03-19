from app.schemas.base_schema import BaseSchema


class CreateRoleSchema(BaseSchema):
    role_name: str
    description: str

class AssignRoleSchema(BaseSchema):
    role_id: str
    user_id: str

class RemoveUserRoleSchema(AssignRoleSchema):
    pass

class DeleteRoleSchema(CreateRoleSchema):
    pass