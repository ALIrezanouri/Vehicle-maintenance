"""
Database connection module for FastAPI MashinMan project.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import get_settings

_settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    def connect(cls):
        """Initialize database connection"""
        cls.client = AsyncIOMotorClient(
            _settings.MONGODB_URL,
            username=_settings.MONGODB_USERNAME,
            password=_settings.MONGODB_PASSWORD,
        )
        cls.db = cls.client[_settings.MONGODB_DB]

    @classmethod
    def close(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance"""
        return cls.db

# Create global database instance
db = Database()

async def get_database() -> AsyncIOMotorDatabase:
    """Dependency for FastAPI to get database instance"""
    return db.get_db()