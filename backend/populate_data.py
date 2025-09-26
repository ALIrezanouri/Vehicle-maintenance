import asyncio
import random
from datetime import datetime, timedelta, date
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from vehicles.models import Vehicle
from services.models import Service
from history.models import ServiceHistory
from emergency.models import EmergencyRequest, EmergencyServiceProvider
from users.models import User
from core.config import Settings

# Sample data
VEHICLE_BRANDS = ["پژو", "سمند", "دنا", "پراید", "Quick"]
VEHICLE_MODELS = ["206", "207", "SE", "Plus", "SL", "SX", "Active", "Tonic"]
SERVICE_TYPES = [
    "تعویض روغن", "چرخش تایر", "بررسی ترمز", "تعویض فیلتر هوا", 
    "تعویض فیلتر روغن", "تعویض جرقه زن", "تعمیر موتور", "بررسی سیستم خنک کننده",
    "تعویض کمک فنر", "بررسی سیستم تعلیق", "تعویض لنت ترمز", "بررسی سیستم برق"
]
EMERGENCY_TYPES = [
    "ترکیدگی لاستیک", "مشکل موتور", "تصادف", "تمام شدن سوخت",
    "قفل شدن درون خودرو", "مشکل برق", "مشکل ترمز", "سایر"
]
NAMES = [
    "علی محمدی", "مریم رضوی", "حسین احمدی", "فاطمه کریمی", "مهدی نوری",
    "سارا حسینی", "رضا صفری", "زهرا رمضانی", "امیر محمودی", "نرگس اسلامی",
    "محمد تقی", "لیلا مرادی", " Abbas حامدی", "نازنین نیکو", "کامران رستمی"
]
PHONE_NUMBERS = [
    "09121111111", "09122222222", "09123333333", "09124444444", "09125555555",
    "09126666666", "09127777777", "09128888888", "09129999999", "09130000000",
    "09131111111", "09132222222", "09133333333", "09134444444", "09135555555"
]

async def init_db():
    """Initialize database connection"""
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.MONGODB_DB], document_models=[
        User, Vehicle, Service, ServiceHistory, EmergencyRequest, EmergencyServiceProvider
    ])

async def create_users(count=20):
    """Create sample users"""
    users = []
    for i in range(count):
        user = User(
            name=NAMES[i % len(NAMES)],
            phone=PHONE_NUMBERS[i % len(PHONE_NUMBERS)],
            email=f"user{i}@example.com",
            password="password123",  # In a real app, this should be hashed
            is_active=True
        )
        users.append(user)
    await User.insert_many(users)
    return users

async def create_vehicles(users, count=50):
    """Create sample vehicles"""
    vehicles = []
    for i in range(count):
        user = random.choice(users)
        brand = random.choice(VEHICLE_BRANDS)
        model = random.choice(VEHICLE_MODELS)
        year = random.randint(1380, 1403)
        license_plate = f"{random.randint(100, 999)}{random.choice(['الف', 'ب', 'پ', 'ت', 'ث'])}{random.randint(100, 999)}"
        current_mileage = random.randint(10000, 200000)
        
        # Generate a date within the last year for last_service_date
        days_ago = random.randint(0, 365)
        last_service_date = date.today() - timedelta(days=days_ago)
        
        vehicle = Vehicle(
            user_id=str(user.id),
            license_plate=license_plate,
            brand=brand,
            model=model,
            manufacture_year=year,
            current_mileage=current_mileage,
            last_service_date=last_service_date,
            last_service_mileage=current_mileage - random.randint(5000, 15000),
            created_at=datetime.now()
        )
        vehicles.append(vehicle)
    await Vehicle.insert_many(vehicles)
    return vehicles

async def create_services(vehicles, count=100):
    """Create sample services"""
    services = []
    for i in range(count):
        vehicle = random.choice(vehicles)
        service_type = random.choice(SERVICE_TYPES)
        cost = random.randint(50000, 1000000)
        status = random.choice(["completed", "in_progress", "pending"])
        priority = random.choice(["low", "medium", "high", "critical"])
        
        # Generate a date within the last year
        days_ago = random.randint(0, 365)
        scheduled_date = date.today() - timedelta(days=days_ago)
        
        service = Service(
            vehicle_id=str(vehicle.id),
            user_id=vehicle.user_id,
            service_type=service_type,
            description=f"سرویس {service_type} برای خودرو {vehicle.brand} {vehicle.model}",
            status=status,
            priority=priority,
            scheduled_date=scheduled_date,
            scheduled_mileage=vehicle.current_mileage + random.randint(5000, 15000),
            actual_date=scheduled_date if status == "completed" else None,
            actual_mileage=vehicle.current_mileage if status == "completed" else None,
            cost=cost if status == "completed" else None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        services.append(service)
    await Service.insert_many(services)
    return services

async def create_service_history(services, count=150):
    """Create sample service history records"""
    history_records = []
    for i in range(count):
        service = random.choice(services)
        parts = random.sample(SERVICE_TYPES, k=random.randint(0, 3))
        description = f"این سرویس شامل {', '.join(parts) if parts else 'بررسی کلی'} می‌شود."
        
        history_record = ServiceHistory(
            service_id=str(service.id),
            vehicle_id=service.vehicle_id,
            service_name=service.service_type,
            cost=service.cost,
            date=service.scheduled_date,
            parts=parts,
            description=description
        )
        history_records.append(history_record)
    await ServiceHistory.insert_many(history_records)
    return history_records

async def create_emergency_services(users, count=30):
    """Create sample emergency services"""
    emergencies = []
    for i in range(count):
        user = random.choice(users)
        emergency_type = random.choice(EMERGENCY_TYPES)
        status = random.choice(["completed", "in_progress", "pending"])
        priority = random.choice(["low", "medium", "high", "critical"])
        
        # Generate a date within the last 30 days
        days_ago = random.randint(0, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        emergency = EmergencyRequest(
            user_id=str(user.id),
            name=user.name,
            phone=user.phone,
            license_plate=f"{random.randint(100, 999)}{random.choice(['الف', 'ب', 'پ', 'ت', 'ث'])}{random.randint(100, 999)}",
            brand=random.choice(VEHICLE_BRANDS),
            model=random.choice(VEHICLE_MODELS),
            latitude=35.6892 + random.uniform(-0.1, 0.1),  # Tehran coordinates with some variation
            longitude=51.3890 + random.uniform(-0.1, 0.1),
            address=f"خیابان {random.randint(1, 200)}، کوچه {random.randint(1, 50)}",
            emergency_type=emergency_type,
            description=f"درخواست اضطراری برای {emergency_type}",
            priority=priority,
            status=status,
            created_at=created_at,
            updated_at=created_at
        )
        emergencies.append(emergency)
    await EmergencyRequest.insert_many(emergencies)
    return emergencies

async def create_emergency_service_providers(count=15):
    """Create sample emergency service providers"""
    providers = []
    for i in range(count):
        provider = EmergencyServiceProvider(
            name=f"خدمات اضطراری {random.choice(['الف', 'ب', 'پ', 'ت', 'ث'])}",
            phone=f"0912{random.randint(1000000, 9999999)}",
            email=f"provider{i}@emergency.ir",
            service_areas=[f"منطقه {j}" for j in range(1, random.randint(2, 6))],
            service_types=random.sample(EMERGENCY_TYPES, k=random.randint(2, 5)),
            latitude=35.6892 + random.uniform(-0.5, 0.5),
            longitude=51.3890 + random.uniform(-0.5, 0.5),
            address=f"آدرس ارائه‌دهنده خدمات {i}",
            is_active=True,
            is_verified=random.choice([True, False])
        )
        providers.append(provider)
    await EmergencyServiceProvider.insert_many(providers)
    return providers

async def main():
    """Main function to populate database with sample data"""
    print("Initializing database...")
    await init_db()
    
    print("Creating users...")
    users = await create_users(20)
    
    print("Creating vehicles...")
    vehicles = await create_vehicles(users, 50)
    
    print("Creating services...")
    services = await create_services(vehicles, 100)
    
    print("Creating service history...")
    await create_service_history(services, 150)
    
    print("Creating emergency services...")
    await create_emergency_services(users, 30)
    
    print("Creating emergency service providers...")
    await create_emergency_service_providers(15)
    
    print("Database populated successfully!")

if __name__ == "__main__":
    asyncio.run(main())