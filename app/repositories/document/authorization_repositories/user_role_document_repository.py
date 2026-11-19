from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authorization_repositories_interfaces.user_role_repository_interface import \
    UserRoleRepositoryInterface


class UserRoleDocumentRepository(BaseDocumentRepository, UserRoleRepositoryInterface):

    async def find_by_role_id(self, role_id: UUID, **kwargs):
        options = kwargs.get("options")
        result = self._collection.find(
            {
                "role_id": role_id
            },
            options
        )
        return await result.to_list()

    async def find_by_user_id(self, user_id: UUID, **kwargs):
        options = kwargs.get("options")
        result = self._collection.find(
            {
                "user_id": user_id
            },
            options
        )
        return await result.to_list()

    async def find_by_user_ids(self, user_ids: list, **kwargs):
        options = kwargs.get("options")
        result = self._collection.find(
            {
                "user_id":
                    {
                        "$in": user_ids
                    }
            },
            options
        )
        return await result.to_list()

    async def delete_many_by_role_id(self, role_id: UUID):
        await self._collection.delete_many(
            {
                "role_id": role_id
            }
        )

    async def get_user_ids_by_role_id(self, role_id: UUID):
        user_role_pipeline = [
            {
            # Get every document with the role_id in argument
                "$match": {
                    "role_id": role_id
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
        result = await result.to_list()

        return result[0] if len(result) > 0 else None

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
