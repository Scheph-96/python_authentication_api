from app.schemas.base_schema import BaseSchema


class CreatePermissionSchema(BaseSchema):
    permission_name: str

class AssignPermissionToRole(BaseSchema):
    role_id: str
    permission_id: str

class RemovePermissionFromRole(AssignPermissionToRole):
    pass

class DeletePermission(BaseSchema):
    pass