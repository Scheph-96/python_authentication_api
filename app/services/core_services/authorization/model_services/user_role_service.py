from app.repositories.authorization_repositories.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository

    async def create_user_role(self, data: dict):
        return await self.user_role_repository.create(data)

    async def find_user_role_by_id(self, user_role_id: str):
        return await self.user_role_repository.find_by_id(user_role_id)

    def find_user_role_by_role_id(self, role_id: str) -> list:
        return self.user_role_repository.find_by_role_id(role_id)

    def find_user_role_by_user_id(self, user_id: str) -> list:
        return self.user_role_repository.find_by_user_id(user_id)

    async def update_user_role(self, user_role_id: str, data: dict):
        await self.user_role_repository.update(user_role_id, data)

    async def delete_user_role(self, user_role_id: str):
        await self.user_role_repository.delete(user_role_id)