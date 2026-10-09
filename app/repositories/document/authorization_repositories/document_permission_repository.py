from app.repositories.document.document_base_repository import DocumentBaseRepository
from app.repositories.interfaces.authorization_repositories.permission_repository_interface import \
    PermissionRepositoryInterface


class PermissionRepository(DocumentBaseRepository, PermissionRepositoryInterface):

    async def find_by_name(self, permission_name: str, options: dict = None):
        return await self._collection.find_one({"permission_name": permission_name}, options)

    async def find_by_name_in(self, permissions_names: list, options: dict = None):
        result = self._collection.find({"permission_name": {"$in": permissions_names}}, options)
        return await result.to_list()

    async def find_by_ids(self, permission_ids: list, options: dict = None):
        result = self._collection.find({"_id": {"$in": permission_ids}}, options)
        return await result.to_list()