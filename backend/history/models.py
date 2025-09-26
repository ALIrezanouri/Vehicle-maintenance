"""
History models for FastAPI MashinMan project using Beanie ODM.
"""

from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import BaseModel, Field, validator
import jdatetime
from core.jalali import gregorian_to_jalali, jalali_to_gregorian
from core.utils import format_persian_number


class ServicePart(BaseModel):
    """
    Service part model for tracking parts used in services.
    """
    name: str = Field(..., description="نام قطعه")
    quantity: int = Field(..., description="تعداد")
    unit_price: int = Field(..., description="قیمت واحد (ریال)")
    total_price: int = Field(..., description="قیمت کل (ریال)")


class ServiceHistory(Document):
    """
    Service history model for tracking completed services.
    """
    
    # References
    service_id: str = Field(..., description="شناسه سرویس")
    vehicle_id: str = Field(..., description="شناسه خودرو")
    user_id: str = Field(..., description="شناسه کاربر")
    
    # Service details
    service_name: str = Field(..., description="نام سرویس")
    service_description: Optional[str] = Field(None, description="توضیحات سرویس")
    service_type: str = Field(..., description="نوع سرویس")
    
    # Vehicle information at time of service
    vehicle_license_plate: str = Field(..., description="شماره پلاک خودرو")
    vehicle_brand: str = Field(..., description="برند خودرو")
    vehicle_model: str = Field(..., description="مدل خودرو")
    vehicle_manufacture_year: int = Field(..., description="سال تولید خودرو")
    
    # Service execution details
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    actual_date: date = Field(..., description="تاریخ واقعی انجام")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    actual_mileage: int = Field(..., description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    
    # Parts used
    parts: List[ServicePart] = Field(default=[], description="قطعات استفاده شده")
    
    # Cost details
    total_cost: int = Field(..., description="هزینه کل سرویس (ریال)")
    parts_cost: int = Field(..., description="هزینه قطعات (ریال)")
    labor_cost: int = Field(..., description="هزینه دست‌مزد (ریال)")
    
    # Service provider information
    service_center_name: Optional[str] = Field(None, description="نام مرکز سرویس")
    technician_name: Optional[str] = Field(None, description="نام تکنسین")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "service_histories"


# Pydantic models for API
class ServiceHistoryCreate(BaseModel):
    """
    Schema for creating a new service history record.
    """
    service_id: str = Field(..., description="شناسه سرویس")
    vehicle_id: str = Field(..., description="شناسه خودرو")
    user_id: str = Field(..., description="شناسه کاربر")
    service_name: str = Field(..., description="نام سرویس")
    service_description: Optional[str] = Field(None, description="توضیحات سرویس")
    service_type: str = Field(..., description="نوع سرویس")
    vehicle_license_plate: str = Field(..., description="شماره پلاک خودرو")
    vehicle_brand: str = Field(..., description="برند خودرو")
    vehicle_model: str = Field(..., description="مدل خودرو")
    vehicle_manufacture_year: int = Field(..., description="سال تولید خودرو")
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    actual_date: date = Field(..., description="تاریخ واقعی انجام")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    actual_mileage: int = Field(..., description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    parts: List[ServicePart] = Field(default=[], description="قطعات استفاده شده")
    total_cost: int = Field(..., description="هزینه کل سرویس (ریال)")
    parts_cost: int = Field(..., description="هزینه قطعات (ریال)")
    labor_cost: int = Field(..., description="هزینه دست‌مزد (ریال)")
    service_center_name: Optional[str] = Field(None, description="نام مرکز سرویس")
    technician_name: Optional[str] = Field(None, description="نام تکنسین")


class ServiceHistoryUpdate(BaseModel):
    """
    Schema for updating a service history record.
    """
    service_id: Optional[str] = Field(None, description="شناسه سرویس")
    vehicle_id: Optional[str] = Field(None, description="شناسه خودرو")
    user_id: Optional[str] = Field(None, description="شناسه کاربر")
    service_name: Optional[str] = Field(None, description="نام سرویس")
    service_description: Optional[str] = Field(None, description="توضیحات سرویس")
    service_type: Optional[str] = Field(None, description="نوع سرویس")
    vehicle_license_plate: Optional[str] = Field(None, description="شماره پلاک خودرو")
    vehicle_brand: Optional[str] = Field(None, description="برند خودرو")
    vehicle_model: Optional[str] = Field(None, description="مدل خودرو")
    vehicle_manufacture_year: Optional[int] = Field(None, description="سال تولید خودرو")
    scheduled_date: Optional[date] = Field(None, description="تاریخ برنامه‌ریزی شده")
    actual_date: Optional[date] = Field(None, description="تاریخ واقعی انجام")
    scheduled_mileage: Optional[int] = Field(None, description="کیلومتر برنامه‌ریزی شده")
    actual_mileage: Optional[int] = Field(None, description="کیلومتر واقعی انجام")
    duration: Optional[int] = Field(None, description="مدت زمان انجام (دقیقه)")
    parts: Optional[List[ServicePart]] = Field(None, description="قطعات استفاده شده")
    total_cost: Optional[int] = Field(None, description="هزینه کل سرویس (ریال)")
    parts_cost: Optional[int] = Field(None, description="هزینه قطعات (ریال)")
    labor_cost: Optional[int] = Field(None, description="هزینه دست‌مزد (ریال)")
    service_center_name: Optional[str] = Field(None, description="نام مرکز سرویس")
    technician_name: Optional[str] = Field(None, description="نام تکنسین")


class ServiceHistoryOut(ServiceHistoryCreate):
    """
    Schema for service history output with additional fields.
    """
    id: str = Field(..., description="شناسه تاریخچه سرویس")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")
