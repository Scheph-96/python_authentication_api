from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


class BaseRepository:
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

    def __init__(self, collection: AsyncIOMotorCollection):
        self._collection = collection
        
    async def create(self, data: dict):
        result = await self._collection.insert_one(data)
        return str(result.inserted_id)

    async def find(self, data: dict, options: dict = None):
        return await self._collection.find_one(data, options)
    
    async def find_by_id(self, id: str, options: dict = None):
        return await self._collection.find_one({"_id": ObjectId(id)}, options)
    
    async def find_all(self, options: dict = None):
        result = self._collection.find({}, options)
        return await result.to_list()
    
    async def update(self, id: str, data: dict):
        return await self._collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        
    async def delete_one(self, id: str):
        await self._collection.delete_one({"_id": ObjectId(id)})

    async def delete_many(self, id: str):
        await self._collection.delete_many({"_id": ObjectId(id)})

    async def delete_many_in(self, ids: list):
        await self._collection.delete_many({"_id": {"$in": ids}})