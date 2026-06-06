class BaseRepositoryInterface:
    def __init__(self, collection):
        self._collection = collection

    async def create(self):
        pass

    async def create_many(self):
        pass

    async def find(self):
        pass

    async def find_by_id(self):
        pass

    async def find_all(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass

    async def delete_one(self):
        pass

    async def delete_many(self):
        pass

    async def delete_many_in(self):
        pass
