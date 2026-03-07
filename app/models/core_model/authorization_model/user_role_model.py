from bson import ObjectId


class UserRole:
    def __init__(self, user_id: ObjectId, role_id: ObjectId, _id: ObjectId=None):
        self.user_id = user_id
        self.role_id = role_id
        self._id = _id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "role_id": self.role_id
        }