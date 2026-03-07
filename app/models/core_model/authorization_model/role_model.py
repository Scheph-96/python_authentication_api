from bson import ObjectId


class Role:
    def __init(self, role_name: str, _id: ObjectId=None):
        self.role_name = role_name
        self._id = _id

    def to_dict(self) -> dict:
        return {
            "role_name": self.role_name
        }