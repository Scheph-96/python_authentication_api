from bson import ObjectId

from app.repositories.base_repository import BaseRepository


class UserRoleRepository(BaseRepository):

    async def find_by_role_id(self, role_id: str, options: dict = None):
        result = self._collection.find({"role_id": ObjectId(role_id)}, options)
        return await result.to_list()

    async def find_by_user_id(self, user_id: str, options: dict = None):
        result = self._collection.find({"user_id": ObjectId(user_id)}, options)
        return await result.to_list()

    async def find_by_user_ids(self, user_ids: list, options: dict = None):
        result = self._collection.find({"user_id": {"$in": user_ids}}, options)
        return await result.to_list()

    async def delete_many_by_role_id(self, role_id: str):
        await self._collection.delete_many({"role_id": ObjectId(role_id)})

    async def get_user_ids_by_role_id(self, role_id: str):
        user_role_pipeline = [
            {
            # Get the role very document with this role
                "$match": {
                    "role_id": ObjectId(role_id)
                }
            },
            # Group users by nothing, because we just
            # want a list of user_ids
            {
                "$group": {
                    "_id": None,
                    "user_ids": {
                        "$push": "$user_id"
                    }
                }
            },
            # Just output the list
            {
                "$project": {
                    "_id": 0,
                    "user_ids": 1
                }
            }
        ]

        result = self._collection.aggregate(user_role_pipeline)
        return await result.to_list()

    async def get_users_and_permissions(self, user_ids: list):

        pipeline = [
            # Get a list users matching the ids
            {
                "$match": {
                    "user_id": {
                        "$in": user_ids
                    }
                }
            },
            # Left join user_role and role_permissions
            {
                "$lookup": {
                    "from": "role_permissions",
                    "localField": "role_id",
                    "foreignField": "role_id",
                    "as": "col_role_permissions"
                }
            },
            # The new field "col_role_permissions" is
            # returned as a list we have to return each
            # document to make it more usable
            {
                "$unwind": "$col_role_permissions"
            },
            # Left join role_permissions and permissions
            {
                "$lookup": {
                    "from": "permissions",
                    "localField": "col_role_permissions.permission_id",
                    "foreignField": "_id",
                    "as": "col_permissions"
                }
            },
            # The new field "col_role_permissions" is
            # returned as a list we have to return each
            # document to make it more usable
            {
                "$unwind": "$col_permissions"
            },
            # Group permissions by user_id
            {
                "$group": {
                    "_id": "$user_id",
                    "permissions": {
                        "$push": "$col_permissions.permission_name"
                    }
                }
            },
            # Build the result output as {"user_id": ..., "permissions": [...]}
            {
                "$project": {
                    "_id": 0,
                    "user_id": "$_id",
                    "permissions": 1
                }
            }
        ]

        result = self._collection.aggregate(pipeline)
        return await result.to_list()
