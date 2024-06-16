import motor.motor_asyncio
from functions.schedule import Var

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.req_one = self.db.reqone
        self.req_two = self.db.reqtwo
      
    async def add_req_one(self, user_id):
        try:
            await self.req_one.insert_one({"user_id": int(user_id)})
            return
        except Exception as e:
            print(e)
            pass
        
    async def add_req_two(self, user_id):
        try:
            await self.req_two.insert_one({"id": int(user_id)})
            return
        except Exception as e:
            print(e)
            pass
            
    async def get_req_one(self, user_id):
        return await self.req_one.find_one({"user_id": int(user_id)})

    async def get_req_two(self, user_id):
        return await self.req_two.find_one({"id": int(user_id)})

    async def delete_all_one(self):
        await self.req_one.delete_many({})

    async def delete_all_two(self):
        await self.req_two.delete_many({})

    async def get_all_one_count(self): 
        count = 0
        async for req in self.req_one.find({}):
            count += 1
        return count

    async def get_all_two_count(self): 
        count = 0
        async for req in self.req_two.find({}):
            count += 1
        return count
        
mdb = Database(Var.MDB_URI, Var.MDB_NAME)
