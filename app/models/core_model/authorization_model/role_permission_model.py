from bson import ObjectId


class RolePermission:
    def __init__(self, role_id: ObjectId, permission_id: ObjectId, _id: ObjectId=None):
        self.role_id = role_id
        self.permission_id = permission_id
        self._id = _id

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "permission_id": self.permission_id
        }