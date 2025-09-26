"""
User models for FastAPI MashinMan project using Beanie ODM.
"""

from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from core.security import get_password_hash, verify_password


class User(Document):
    """
    User model for MashinMan using Beanie ODM.
    """
    
    # Basic user information
    name: str = Field(..., max_length=100, description="نام")
    phone: str = Field(..., max_length=15, unique=True, description="شماره تلفن")
    email: Optional[EmailStr] = Field(None, description="ایمیل")
    password: str = Field(..., description="رمز عبور")
    
    # User status and timestamps
    is_active: bool = Field(default=True, description="فعال")
    is_verified: bool = Field(default=False, description="تایید شده")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="تاریخ ایجاد")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="تاریخ بروزرسانی")
    last_login: Optional[datetime] = Field(None, description="آخرین ورود")
    
    # Profile information
    avatar: Optional[str] = Field(None, description="تصویر پروفایل")
    birth_date: Optional[datetime] = Field(None, description="تاریخ تولد")
    city: Optional[str] = Field(None, max_length=50, description="شهر")
    
    # Notification preferences
    sms_notifications: bool = Field(default=True, description="اعلان پیامکی")
    email_notifications: bool = Field(default=True, description="اعلان ایمیل")
    push_notifications: bool = Field(default=True, description="اعلان اپلیکیشن")
    
    # Emergency contact
    emergency_contact_name: Optional[str] = Field(None, max_length=100, description="نام مخاطب اضطراری")
    emergency_contact_phone: Optional[str] = Field(None, max_length=15, description="تلفن مخاطب اضطراری")
    
    class Settings:
        name = "users"
        indexes = [
            "phone",
            "email",
            "created_at",
        ]
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hashed password"""
        return verify_password(password, self.password)
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a password"""
        return get_password_hash(password)







class Token(BaseModel):
    """JWT Token model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data model"""
    user_id: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(BaseModel):
    """User creation model"""
    name: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=15)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    city: Optional[str] = Field(None, max_length=50)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=15)


class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    city: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = None
    birth_date: Optional[datetime] = None
    sms_notifications: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=15)


class UserOut(BaseModel):
    """User output model"""
    id: str
    name: str
    phone: str
    email: Optional[EmailStr] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    avatar: Optional[str] = None
    birth_date: Optional[datetime] = None
    city: Optional[str] = None
    sms_notifications: bool
    email_notifications: bool
    push_notifications: bool
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
