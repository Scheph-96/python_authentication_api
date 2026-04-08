from app.core.errors.domain_errors import DomainErrors


class RoleAlreadyExists(DomainErrors):
    def __init__(self, role_name: str):
        super().__init__(message=f"Role: `{role_name}` already exists")


class PermissionAlreadyExists(DomainErrors):
    def __init__(self, permission_name: str):
        super().__init__(message=f"Permission: `{permission_name}` already exists")


class RoleNotFound(DomainErrors):
    def __init__(self, role_id: str):
        super().__init__(message=f"Role ID: `{role_id}` does not exist")


class PermissionNotFound(DomainErrors):
    def __init__(self, permission_id: str):
        super().__init__(message=f"Permission ID: `{permission_id}` does not exist")


class UserNotFound(DomainErrors):
    def __init__(self, user_id):
        super().__init__(message=f"User ID: `{user_id}` does not exist")


class RoleAlreadyAssigned(DomainErrors):
    def __init__(self, role_id: str):
        super().__init__(message=f"Role ID: `{role_id}` already assigned")


class PermissionAlreadyAssigned(DomainErrors):
    def __init__(self, permission_id: str):
        super().__init__(message=f"Permission ID: `{permission_id}` already assigned")


class RoleNotAssigned(DomainErrors):
    def __init__(self, role_id: str):
        super().__init__(message=f"Role ID: `{role_id}` is not assigned")

class PermissionNotAssigned(DomainErrors):
    def __init__(self, permission_id: str):
        super().__init__(message=f"Permission ID: `{permission_id} is not assigned`")