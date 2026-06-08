from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from sqlalchemy import Table

from app.repositories.interfaces.base_repository_interface import BaseRepositoryInterface
from app.utils.resources import dict_string_to_objectid


class BaseRepository(BaseRepositoryInterface):
    """
        Parent repository

        FYI: In some children repositories we can see this:

            result = self._collection.find({...})
            return await result.to_list()

        First of all `find` is not awaited, as mentioned in the documentation:

            `Note that find does not require an await expression, because
             find merely creates a MotorCursor without performing any
             operations on the server. MotorCursor methods such as to_list()
             perform actual operations.`

        Secondly, `find` query return an `AsyncIOMotorCursor` object while
        we expect a list. To fix that we call the `to_list` function of
        `AsyncIOMotorCursor`, that function return a list containing the
        result of the query(what we actually expect). That `to_list` function
        is the operation that is actually awaited

        For more information: https://motor.readthedocs.io/en/stable/index.html
    """

    def __init__(self, collection: Table):
        super().__init__(collection)

    async def create(self, data: dict):
        Table.insert(self._collection).values()

    async def create_many(self):
        return await super().create_many()

    async def find(self):
        return await super().find()

    async def find_by_id(self):
        return await super().find_by_id()

    async def find_all(self):
        return await super().find_all()

    async def update(self):
        return await super().update()

    async def delete(self):
        return await super().delete()

    async def delete_one(self):
        return await super().delete_one()

    async def delete_many(self):
        return await super().delete_many()

    async def delete_many_in(self):
        return await super().delete_many_in()
