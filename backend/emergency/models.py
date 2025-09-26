"""
Emergency models for FastAPI MashinMan project using Beanie ODM with Jalali calendar support.
"""

from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import BaseModel, Field, validator
import jdatetime
from core.utils import validate_phone_number, sanitize_input
from core.exceptions import EmergencyRequestFailedException
from core.jalali import gregorian_to_jalali, jalali_to_gregorian


class EmergencyRequest(Document):
    """
    Emergency request model for tracking emergency service requests.
    """
    
    # User information
    user_id: str = Field(..., description="شناسه کاربر")
    name: str = Field(..., description="نام درخواست‌کننده")
    phone: str = Field(..., description="شماره تماس")
    
    # Vehicle information
    vehicle_id: Optional[str] = Field(None, description="شناسه خودرو")
    license_plate: str = Field(..., description="شماره پلاک خودرو")
    brand: Optional[str] = Field(None, description="برند خودرو")
    model: Optional[str] = Field(None, description="مدل خودرو")
    
    # Location information
    latitude: float = Field(..., description="عرض جغرافیایی")
    longitude: float = Field(..., description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")
    
    # Emergency details
    emergency_type: str = Field(..., description="نوع اضطراری")
    description: Optional[str] = Field(None, description="توضیحات")
    priority: str = Field(default="medium", description="اولویت")
    
    # Status tracking
    status: str = Field(default="pending", description="وضعیت")
    assigned_to: Optional[str] = Field(None, description="شناسه اعزام‌شده")
    response_time: Optional[int] = Field(None, description="زمان پاسخ (ثانیه)")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "emergency_requests"
    
    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError("شماره تلفن نامعتبر است")
        return v
    
    @validator('name')
    def sanitize_name(cls, v):
        return sanitize_input(v) if v else v


# Emergency service provider model
class EmergencyServiceProvider(Document):
    """
    Emergency service provider model for tracking service providers.
    """
    
    # Provider information
    name: str = Field(..., description="نام ارائه‌دهنده")
    phone: str = Field(..., description="شماره تماس")
    email: Optional[str] = Field(None, description="ایمیل")
    
    # Service area
    service_areas: List[str] = Field(default=[], description="مناطق تحت پوشش")
    service_types: List[str] = Field(default=[], description="انواع خدمات ارائه شده")
    
    # Location
    latitude: Optional[float] = Field(None, description="عرض جغرافیایی")
    longitude: Optional[float] = Field(None, description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")
    
    # Status
    is_active: bool = Field(default=True, description="وضعیت فعال بودن")
    is_verified: bool = Field(default=False, description="وضعیت تأیید")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "emergency_service_providers"


# Pydantic models for API
class EmergencyRequestCreate(BaseModel):
    """
    Schema for creating a new emergency request.
    """
    user_id: str = Field(..., description="شناسه کاربر")
    name: str = Field(..., description="نام درخواست‌کننده")
    phone: str = Field(..., description="شماره تماس")
    vehicle_id: Optional[str] = Field(None, description="شناسه خودرو")
    license_plate: str = Field(..., description="شماره پلاک خودرو")
    brand: Optional[str] = Field(None, description="برند خودرو")
    model: Optional[str] = Field(None, description="مدل خودرو")
    latitude: float = Field(..., description="عرض جغرافیایی")
    longitude: float = Field(..., description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")
    emergency_type: str = Field(..., description="نوع اضطراری")
    description: Optional[str] = Field(None, description="توضیحات")
    priority: str = Field(default="medium", description="اولویت")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError("شماره تلفن نامعتبر است")
        return v
    
    @validator('name')
    def sanitize_name(cls, v):
        return sanitize_input(v) if v else v


class EmergencyServiceProviderCreate(BaseModel):
    """
    Schema for creating a new emergency service provider.
    """
    name: str = Field(..., description="نام ارائه‌دهنده")
    phone: str = Field(..., description="شماره تماس")
    email: Optional[str] = Field(None, description="ایمیل")
    service_areas: List[str] = Field(default=[], description="مناطق تحت پوشش")
    service_types: List[str] = Field(default=[], description="انواع خدمات ارائه شده")
    latitude: Optional[float] = Field(None, description="عرض جغرافیایی")
    longitude: Optional[float] = Field(None, description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")


class EmergencyRequestUpdate(BaseModel):
    """
    Schema for updating an emergency request.
    """
    user_id: Optional[str] = Field(None, description="شناسه کاربر")
    name: Optional[str] = Field(None, description="نام درخواست‌کننده")
    phone: Optional[str] = Field(None, description="شماره تماس")
    vehicle_id: Optional[str] = Field(None, description="شناسه خودرو")
    license_plate: Optional[str] = Field(None, description="شماره پلاک خودرو")
    brand: Optional[str] = Field(None, description="برند خودرو")
    model: Optional[str] = Field(None, description="مدل خودرو")
    latitude: Optional[float] = Field(None, description="عرض جغرافیایی")
    longitude: Optional[float] = Field(None, description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")
    emergency_type: Optional[str] = Field(None, description="نوع اضطراری")
    description: Optional[str] = Field(None, description="توضیحات")
    priority: Optional[str] = Field(None, description="اولویت")
    status: Optional[str] = Field(None, description="وضعیت")
    assigned_to: Optional[str] = Field(None, description="شناسه اعزام‌شده")
    response_time: Optional[int] = Field(None, description="زمان پاسخ (ثانیه)")
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is not None and not validate_phone_number(v):
            raise ValueError("شماره تلفن نامعتبر است")
        return v
    
    @validator('name')
    def sanitize_name(cls, v):
        return sanitize_input(v) if v else v


class EmergencyServiceProviderUpdate(BaseModel):
    """
    Schema for updating an emergency service provider.
    """
    name: Optional[str] = Field(None, description="نام ارائه‌دهنده")
    phone: Optional[str] = Field(None, description="شماره تماس")
    email: Optional[str] = Field(None, description="ایمیل")
    service_areas: Optional[List[str]] = Field(None, description="مناطق تحت پوشش")
    service_types: Optional[List[str]] = Field(None, description="انواع خدمات ارائه شده")
    latitude: Optional[float] = Field(None, description="عرض جغرافیایی")
    longitude: Optional[float] = Field(None, description="طول جغرافیایی")
    address: Optional[str] = Field(None, description="آدرس")
    is_active: Optional[bool] = Field(None, description="وضعیت فعال بودن")
    is_verified: Optional[bool] = Field(None, description="وضعیت تأیید")


class EmergencyRequestOut(EmergencyRequestCreate):
    """
    Schema for emergency request output with additional fields.
    """
    id: str = Field(..., description="شناسه درخواست اضطراری")
    status: str = Field(..., description="وضعیت")
    assigned_to: Optional[str] = Field(None, description="شناسه اعزام‌شده")
    response_time: Optional[int] = Field(None, description="زمان پاسخ (ثانیه)")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")


class EmergencyServiceProviderOut(EmergencyServiceProviderCreate):
    """
    Schema for emergency service provider output with additional fields.
    """
    id: str = Field(..., description="شناسه ارائه‌دهنده خدمات اضطراری")
    is_active: bool = Field(..., description="وضعیت فعال بودن")
    is_verified: bool = Field(..., description="وضعیت تأیید")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")
