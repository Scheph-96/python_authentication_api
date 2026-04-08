from motor.motor_asyncio import AsyncIOMotorCursor

from app.repositories.authorization_repositories.user_role_repository import UserRoleRepository


class UserRoleService:
    """
        The service work with a collection equivalent to a "many-to-many" table
        {
            "role_id": ObjectId(...)
            "user_id": ObjectId(...)
        }

        A role is assigned the many users and many user has the same role
    """
    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository

    async def create_user_role(self, data: dict):
        return await self.user_role_repository.create(data)

    async def find_user_role(self, data: dict, options: dict = None):
        """
            Retrieve a user_role that has a specific role_id and a specific user_id,
            data will look like
            {
                "role_id": ObjectId(...)
                "user_id": ObjectId(...)
            }
            and only one entry will be returned
        :param data:
        :param options:
        :return:
        """
        return await self.user_role_repository.find(data, options)

    async def find_user_role_by_id(self, user_role_id: str):
        return await self.user_role_repository.find_by_id(user_role_id)

    async def find_user_role_by_role_id(self, role_id: str) -> list:
        """
            Retrieve every user_role entries with the specified role_id
        :param role_id:
        :return:
        """
        return await self.user_role_repository.find_by_role_id(role_id)

    async def find_user_role_by_user_id(self, user_id: str, options: dict = None) -> list:
        """
            Retrieve every user_role entries with the specified user_id
        :param user_id:
        :param options:
        :return:
        """
        return await self.user_role_repository.find_by_user_id(user_id, options)

    async def update_user_role(self, user_role_id: str, data: dict):
        await self.user_role_repository.update(user_role_id, data)

    async def delete_user_role(self, user_role_id: str):
        await self.user_role_repository.delete_one(user_role_id)

    async def delete_many_user_role_by_role_id(self, role_id: str):
        await self.user_role_repository.delete_many_by_role_id(role_od)