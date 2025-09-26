"""
Jalali (Persian) calendar date utilities for MashinMan project.
"""

from datetime import date, datetime
import jdatetime


def gregorian_to_jalali(g_date: date) -> str:
    """
    Convert Gregorian date to Jalali date string.
    
    Args:
        g_date (date): Gregorian date
        
    Returns:
        str: Jalali date in YYYY/MM/DD format
    """
    if not g_date:
        return None
    
    j_date = jdatetime.date.fromgregorian(date=g_date)
    return f"{j_date.year:04d}/{j_date.month:02d}/{j_date.day:02d}"


def jalali_to_gregorian(j_date_str: str) -> date:
    """
    Convert Jalali date string to Gregorian date.
    
    Args:
        j_date_str (str): Jalali date in YYYY/MM/DD format
        
    Returns:
        date: Gregorian date
    """
    if not j_date_str:
        return None
    
    try:
        year, month, day = map(int, j_date_str.split('/'))
        g_date = jdatetime.date(year, month, day).togregorian()
        return g_date
    except (ValueError, TypeError):
        raise ValueError(f"Invalid Jalali date format: {j_date_str}. Expected YYYY/MM/DD")


def jalali_now() -> str:
    """
    Get current date in Jalali format.
    
    Returns:
        str: Current date in YYYY/MM/DD format
    """
    today = jdatetime.date.today()
    return f"{today.year:04d}/{today.month:02d}/{today.day:02d}"
"""
Service models for FastAPI MashinMan project using Beanie ODM with Jalali calendar support.
"""

from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import BaseModel, Field, validator
import jdatetime
from core.jalali import gregorian_to_jalali, jalali_to_gregorian, jalali_now
from core.utils import (
    get_service_types,
    calculate_next_service_mileage,
    format_persian_number,
    validate_mileage
)
from core.exceptions import InvalidMileageException

# Service status choices
SERVICE_STATUS_CHOICES = [
    'pending',      # Waiting to be started
    'in_progress',  # Currently being worked on
    'completed',    # Finished successfully
    'cancelled',    # Cancelled by user or system
    'delayed',      # Postponed for some reason
]

# Service priority levels
SERVICE_PRIORITY_CHOICES = [
    'low',      # Routine maintenance
    'medium',   # Standard service
    'high',     # Urgent service
    'critical', # Emergency service
]


class ServiceType(Document):
    """
    Service type model for defining different types of services.
    """
    name: str = Field(..., description="نام نوع سرویس")
    description: Optional[str] = Field(None, description="توضیحات نوع سرویس")
    estimated_duration: Optional[int] = Field(None, description="مدت زمان تخمینی (دقیقه)")
    base_price: Optional[int] = Field(None, description="قیمت پایه سرویس (ریال)")
    is_active: bool = Field(default=True, description="وضعیت فعال بودن")
    
    class Settings:
        name = "service_types"


class Service(Document):
    """
    Service model for tracking vehicle services.
    """
    # Service identification
    vehicle_id: str = Field(..., description="شناسه خودرو")
    user_id: str = Field(..., description="شناسه کاربر")
    service_type: str = Field(..., description="نوع سرویس")
    
    # Service details
    description: Optional[str] = Field(None, description="توضیحات سرویس")
    status: str = Field(default="pending", description="وضعیت سرویس")
    priority: str = Field(default="medium", description="اولویت سرویس")
    
    # Scheduling
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    
    # Execution
    actual_date: Optional[date] = Field(None, description="تاریخ واقعی انجام")
    actual_mileage: Optional[int] = Field(None, description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    
    # Cost
    cost: Optional[int] = Field(None, description="هزینه سرویس (ریال)")
    parts_cost: Optional[int] = Field(None, description="هزینه قطعات (ریال)")
    labor_cost: Optional[int] = Field(None, description="هزینه دست‌مزد (ریال)")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "services"
    
    @validator('service_type')
    def validate_service_type(cls, v):
        service_types = get_service_types()
        if v not in service_types:
            raise ValueError("نوع سرویس نامعتبر است")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in SERVICE_STATUS_CHOICES:
            raise ValueError("وضعیت سرویس نامعتبر است")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in SERVICE_PRIORITY_CHOICES:
            raise ValueError("اولویت سرویس نامعتبر است")
        return v
    
    @validator('actual_mileage', 'scheduled_mileage')
    def validate_mileage_fields(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v


class ServiceReminder(Document):
    """
    Service reminder model for scheduling future services.
    """
    service_id: str = Field(..., description="شناسه سرویس")
    user_id: str = Field(..., description="شناسه کاربر")
    vehicle_id: str = Field(..., description="شناسه خودرو")
    
    # Reminder details
    reminder_type: str = Field(..., description="نوع یادآوری")
    reminder_date: date = Field(..., description="تاریخ یادآوری")
    reminder_mileage: Optional[int] = Field(None, description="کیلومتر یادآوری")
    
    # Status
    is_active: bool = Field(default=True, description="وضعیت فعال بودن")
    is_sent: bool = Field(default=False, description="وضعیت ارسال")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "service_reminders"


class ServiceCenter(Document):
    """
    Service center model for storing information about service centers.
    """
    name: str = Field(..., description="نام مرکز سرویس")
    address: str = Field(..., description="آدرس مرکز سرویس")
    phone: str = Field(..., description="شماره تماس مرکز سرویس")
    latitude: Optional[float] = Field(None, description="عرض جغرافیایی")
    longitude: Optional[float] = Field(None, description="طول جغرافیایی")
    
    # Service capabilities
    services_offered: List[str] = Field(default=[], description="سرویس‌های ارائه شده")
    is_verified: bool = Field(default=False, description="وضعیت تأیید")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "service_centers"


# Pydantic models for API
class ServiceCreate(BaseModel):
    """
    Schema for creating a new service.
    """
    vehicle_id: str = Field(..., description="شناسه خودرو")
    user_id: str = Field(..., description="شناسه کاربر")
    service_type: str = Field(..., description="نوع سرویس")
    description: Optional[str] = Field(None, description="توضیحات سرویس")
    status: str = Field(default="pending", description="وضعیت سرویس")
    priority: str = Field(default="medium", description="اولویت سرویس")
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    actual_date: Optional[date] = Field(None, description="تاریخ واقعی انجام")
    actual_mileage: Optional[int] = Field(None, description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    cost: Optional[int] = Field(None, description="هزینه سرویس (ریال)")
    parts_cost: Optional[int] = Field(None, description="هزینه قطعات (ریال)")
    labor_cost: Optional[int] = Field(None, description="هزینه دست‌مزد (ریال)")
    
    @validator('service_type')
    def validate_service_type(cls, v):
        service_types = get_service_types()
        if v not in service_types:
            raise ValueError("نوع سرویس نامعتبر است")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in SERVICE_STATUS_CHOICES:
            raise ValueError("وضعیت سرویس نامعتبر است")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in SERVICE_PRIORITY_CHOICES:
            raise ValueError("اولویت سرویس نامعتبر است")
        return v
    
    @validator('actual_mileage', 'scheduled_mileage')
    def validate_mileage_fields(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v


class ServiceUpdate(BaseModel):
    """
    Schema for updating a service.
    """
    vehicle_id: Optional[str] = Field(None, description="شناسه خودرو")
    user_id: Optional[str] = Field(None, description="شناسه کاربر")
    service_type: Optional[str] = Field(None, description="نوع سرویس")
    description: Optional[str] = Field(None, description="توضیحات سرویس")
    status: Optional[str] = Field(None, description="وضعیت سرویس")
    priority: Optional[str] = Field(None, description="اولویت سرویس")
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    actual_date: Optional[date] = Field(None, description="تاریخ واقعی انجام")
    actual_mileage: Optional[int] = Field(None, description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    cost: Optional[int] = Field(None, description="هزینه سرویس (ریال)")
    parts_cost: Optional[int] = Field(None, description="هزینه قطعات (ریال)")
    labor_cost: Optional[int] = Field(None, description="هزینه دست‌مزد (ریال)")
    
    @validator('service_type')
    def validate_service_type(cls, v):
        if v is not None:
            service_types = get_service_types()
            if v not in service_types:
                raise ValueError("نوع سرویس نامعتبر است")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in SERVICE_STATUS_CHOICES:
            raise ValueError("وضعیت سرویس نامعتبر است")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in SERVICE_PRIORITY_CHOICES:
            raise ValueError("اولویت سرویس نامعتبر است")
        return v
    
    @validator('actual_mileage', 'scheduled_mileage')
    def validate_mileage_fields(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v


class ServiceOut(ServiceCreate):
    """
    Schema for service output with additional fields.
    """
    id: str = Field(..., description="شناسه سرویس")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")
