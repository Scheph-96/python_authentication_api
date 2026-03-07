from bson import ObjectId


class Permission:
    def __init(self, permission_name: str, _id: ObjectId = None):
        self.permission_name = permission_name
        self._id = _id

    def to_dict(self) -> dict:
        return {
            "permission_name": self.permission_name
        }