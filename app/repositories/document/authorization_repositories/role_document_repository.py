from app.repositories.document.base_document_repository import BaseDocumentRepository
from app.repositories.interfaces.authorization_repositories_interfaces.role_repository_interface import \
    RoleRepositoryInterface


class RoleDocumentRepository(BaseDocumentRepository, RoleRepositoryInterface):

    async def find_by_name(self, role_name: str):
        return await self._collection.find_one({"role_name": role_name})
