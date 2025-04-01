from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None



async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_db():
    if not "fitness-appointment":
        raise ValueError("Database name not configured")
    return client["fitness-appointment"]

async def connect_to_mongo():
    global client
    try:
        client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tlsAllowInvalidCertificates=True
    )
        # Verify connection
        await client.server_info()
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise