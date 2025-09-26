import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from users.models import User
from vehicles.models import Vehicle
from services.models import Service
from emergency.models import EmergencyRequest
from core.config import Settings

async def check_data():
    """Check data in database"""
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.MONGODB_DB], document_models=[
        User, Vehicle, Service, EmergencyRequest
    ])
    
    user_count = await User.find_all().count()
    vehicle_count = await Vehicle.find_all().count()
    service_count = await Service.find_all().count()
    emergency_count = await EmergencyRequest.find_all().count()
    
    print(f"Number of users: {user_count}")
    print(f"Number of vehicles: {vehicle_count}")
    print(f"Number of services: {service_count}")
    print(f"Number of emergency requests: {emergency_count}")

if __name__ == "__main__":
    asyncio.run(check_data())