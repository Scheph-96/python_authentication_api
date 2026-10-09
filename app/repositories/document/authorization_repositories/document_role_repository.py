from app.repositories.document.document_base_repository import DocumentBaseRepository


class RoleRepository(DocumentBaseRepository):

    async def find_by_name(self, role_name: str):
        return await self._collection.find_one({"role_name": role_name})
