from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://hackathon:1234@policy-maker.9zwjcrb.mongodb.net/policy_execution_db?appName=Policy-Maker"

client = None
db = None

def get_db():
    global client, db
    if client is None:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client.get_database()
    return db
