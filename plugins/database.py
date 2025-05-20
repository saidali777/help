import motor.motor_asyncio
from config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.helper_bot_db
users_collection = db.users

async def add_user(user_id: int, username: str):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        await users_collection.insert_one({"_id": user_id, "username": username})

async def get_all_users():
    cursor = users_collection.find({})
    return [user async for user in cursor]

