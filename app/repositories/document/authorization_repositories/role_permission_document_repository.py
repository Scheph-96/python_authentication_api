from uuid import UUID

from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authorization_repositories_interfaces.role_permission_repository_interface import \
    RolePermissionRepositoryInterface


class RolePermissionDocumentRepository(BaseDocumentRepository, RolePermissionRepositoryInterface):

    async def find_by_role_id(self, role_id: str):
        result = self._collection.find({"role_id": UUID(role_id)})
        return await result.to_list()

    async def find_by_role_ids(self, role_ids: list, options: dict = None):
        result = self._collection.find({"role_id": {"$in": role_ids}}, options)
        return await result.to_list()

    async def find_by_permission_id(self, permission_id: str):
        result = self._collection.find({"permission_id": UUID(permission_id)})
        return await result.to_list()

    async def get_user_ids_from_role_permissions(self, permission_id: str):
        pipeline = [
            {
                "$match": {
                    "permission_id": UUID(permission_id)
                }
            },
            {
                "$lookup": {
                    "from": "user_roles",
                    "localField": "role_id",
                    "foreignField": "role_id",
                    "as": "user_roles"
                }
            },
            {
                "$unwind": "$user_roles"
            },
            {
                "$group": {
                    "_id": "$role_id",
                    "user_ids": {
                        "$addToSet": "$user_roles.user_id"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "user_ids": 1
                }
            }
        ]

        result = self._collection.aggregate(pipeline)
        return await result.to_list()

    async def delete_many_by_role_id(self, role_id: str):
        await self._collection.delete_many({"role_id": UUID(role_id)})

    async def delete_many_by_permission_id(self, permission_id: str):
        await self._collection.delete_many({"permission_id": UUID(permission_id)})
