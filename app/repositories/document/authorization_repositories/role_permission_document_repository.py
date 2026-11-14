from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface


class RolePermissionDocumentRepository(BaseDocumentRepository, RolePermissionRepositoryInterface):

    async def find_by_role_id(self, role_id: UUID):
        result = self._collection.find(
            {
                "role_id": role_id
            }
        )
        return await result.to_list()

    async def find_by_role_ids(self, role_ids: list, **kwargs):
        options = kwargs.get("options")
        result = self._collection.find(
            {
                "role_id": {
                    "$in": role_ids
                }
            },
            options
        )
        return await result.to_list()

    async def find_by_permission_id(self, permission_id: UUID):
        result = self._collection.find(
            {
                "permission_id": permission_id
            }
        )
        return await result.to_list()

    async def get_user_ids_from_role_permissions(self, permission_id: UUID):
        """
            Return users that have the provided permission

            Logic
            Find role_permissions matching the permission_id.
            Join with user_roles using role_id.
            Collect unique user_id values.
        """
        pipeline = [
            # Filters role_permissions to keep only records associated with the requested permission_id.
            {
                "$match": {
                    "permission_id": permission_id
                }
            },
            # This performs a join with the user_roles collection.
            # $lookup produces an array of matching documents.
            # Like: {
            #           "role_id": "...",
            #           "permission_id": "...",
            #           "user_roles": [{"user_id": "...", "role_id": "..."}, etc...]
            #       }
            {

                # from: Collection to search in (user_roles).
                # localField: Field in the current documents (role_id).
                # foreignField: Field to match in the other collection (role_id).
                # as: Name of the new field containing the matches.
                #
                # $lookup does not replace the original documents.
                # It adds a new field (user_roles) containing an array of matching documents.

                "$lookup": {
                    "from": "user_roles",
                    "localField": "role_id",
                    "foreignField": "role_id",
                    "as": "user_roles"
                }
            },
            # This expands the user_roles array into individual documents.
            # Which increase the number of documents
            # It takes an array and creates a separate document
            # for each element in that array.
            # {
            #   "role_id": "...",
            #   "permission_id": "...",
            #   "user_roles": {"user_id": "...", "role_id": "..."}
            # }
            # {
            #   "role_id": "...",
            #   "permission_id": "...",
            #   "user_roles": {"user_id": "...", "role_id": "..."}
            # }
            {
                "$unwind": "$user_roles"
            },
            # Now user_id is taken out of each document and put into a Set(to prevent duplication)
            # It reads the value at user_roles.user_id and accumulates it into
            # a new array called user_ids.
            # grouped by None, which only retain the user_ids.
            # The user_ids are the ones of the users who have
            # the permissions passed in argument
            #
            # MongoDB has discarded the other fields (permission_id and user_roles).
            # Only the grouping key and accumulated values remain.
            {
                "$group": {
                    "_id": None,
                    "user_ids": {
                        "$addToSet": "$user_roles.user_id"
                    }
                }
            },
            # And finally in the role_id is discarded and only the list
            # of document containing user_ids is returned. Like
            # [
            #     {"user_ids": [user_1, user_2, user_3, user_4]}
            # ]
            {
                "$project": {
                    "_id": 0,
                    "user_ids": 1
                }
            }
        ]

        result = self._collection.aggregate(pipeline)
        return await result.to_list()

    async def delete_many_by_role_id(self, role_id: UUID):
        await self._collection.delete_many(
            {
                "role_id": role_id
            }
        )

    async def delete_many_by_permission_id(self, permission_id: UUID):
        await self._collection.delete_many(
            {
                "permission_id": permission_id
            }
        )
