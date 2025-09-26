"""
Configuration module for FastAPI MashinMan project.
Replaces Django settings.
"""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import (
    AnyUrl,
    Field,
    field_validator,
)


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "MashinMan"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Security settings
    SECRET_KEY: str = "fastapi-insecure-f8w9h2d9u#_3ev(w!*8v077e8x2#4-5wk68za-@c(rc)qa)opy"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 9000
    
    # MongoDB settings
    MONGODB_DB: str = "mashinman"
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_URL: str = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"
    
    # Redis settings (for caching and sessions)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # 7 days
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Email settings
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = "noreply@mashinman.ir"
    
    # SMS settings
    SMS_PROVIDER: str = "kavenegar"
    SMS_API_KEY: str = ""
    SMS_SENDER: str = "10008663"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STATIC_ROOT: Path = BASE_DIR / 'staticfiles'
    MEDIA_ROOT: Path = BASE_DIR / 'media'
    LOGS_DIR: Path = BASE_DIR / 'logs'
    
    @field_validator('MONGODB_URL')
    def assemble_db_connection(cls, v: str, values) -> str:
        if isinstance(v, str):
            return v
        
        return f"mongodb://{values.data.get('MONGODB_HOST')}:{values.data.get('MONGODB_PORT')}/{values.data.get('MONGODB_DB')}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings instance"""
    return Settings()


# Create settings instance
settings = get_settings()

# Ensure directories exist
settings.STATIC_ROOT.mkdir(exist_ok=True)
settings.MEDIA_ROOT.mkdir(exist_ok=True)
settings.LOGS_DIR.mkdir(exist_ok=True)