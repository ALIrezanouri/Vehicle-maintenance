"""
Vehicle models for FastAPI MashinMan project using Beanie ODM with Jalali calendar support.
"""

from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import BaseModel, Field, validator
import jdatetime  # For Jalali calendar support
from core.utils import (
    validate_iranian_license_plate,
    normalize_license_plate,
    validate_mileage,
    get_iranian_car_brands
)
from core.exceptions import InvalidLicensePlateException, InvalidMileageException


class Vehicle(Document):
    """
    Vehicle model for storing car information using Beanie ODM.
    """
    
    # Vehicle identification
    license_plate: str = Field(..., description="شماره پلاک خودرو")
    brand: str = Field(..., description="برند خودرو")
    model: str = Field(..., description="مدل خودرو")
    manufacture_year: int = Field(..., description="سال تولید")
    
    # Vehicle status
    current_mileage: int = Field(..., description="کیلومتر فعلی")
    last_service_date: Optional[date] = Field(None, description="تاریخ آخرین سرویس")
    last_service_mileage: Optional[int] = Field(None, description="کیلومتر آخرین سرویس")
    
    # Ownership
    user_id: str = Field(..., description="شناسه کاربر مالک")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "vehicles"
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        if not validate_iranian_license_plate(v):
            raise InvalidLicensePlateException()
        return normalize_license_plate(v)
    
    @validator('current_mileage')
    def validate_current_mileage(cls, v):
        if not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('last_service_mileage')
    def validate_last_service_mileage(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('brand')
    def validate_brand(cls, v):
        iranian_brands = get_iranian_car_brands()
        if v not in iranian_brands:
            raise ValueError("برند خودرو نامعتبر است")
        return v
    
    def __repr__(self):
        return f"<Vehicle {self.license_plate}>"


class VehicleCreate(BaseModel):
    """
    Schema for creating a new vehicle.
    """
    license_plate: str = Field(..., description="شماره پلاک خودرو")
    brand: str = Field(..., description="برند خودرو")
    model: str = Field(..., description="مدل خودرو")
    manufacture_year: int = Field(..., description="سال تولید")
    current_mileage: int = Field(..., description="کیلومتر فعلی")
    last_service_date: Optional[date] = Field(None, description="تاریخ آخرین سرویس")
    last_service_mileage: Optional[int] = Field(None, description="کیلومتر آخرین سرویس")
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        if not validate_iranian_license_plate(v):
            raise InvalidLicensePlateException()
        return normalize_license_plate(v)
    
    @validator('current_mileage')
    def validate_current_mileage(cls, v):
        if not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('last_service_mileage')
    def validate_last_service_mileage(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('brand')
    def validate_brand(cls, v):
        iranian_brands = get_iranian_car_brands()
        if v not in iranian_brands:
            raise ValueError("برند خودرو نامعتبر است")
        return v


class VehicleUpdate(BaseModel):
    """
    Schema for updating a vehicle.
    """
    license_plate: Optional[str] = Field(None, description="شماره پلاک خودرو")
    brand: Optional[str] = Field(None, description="برند خودرو")
    model: Optional[str] = Field(None, description="مدل خودرو")
    manufacture_year: Optional[int] = Field(None, description="سال تولید")
    current_mileage: Optional[int] = Field(None, description="کیلومتر فعلی")
    last_service_date: Optional[date] = Field(None, description="تاریخ آخرین سرویس")
    last_service_mileage: Optional[int] = Field(None, description="کیلومتر آخرین سرویس")
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        if v is not None and not validate_iranian_license_plate(v):
            raise InvalidLicensePlateException()
        return normalize_license_plate(v) if v else v
    
    @validator('current_mileage')
    def validate_current_mileage(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('last_service_mileage')
    def validate_last_service_mileage(cls, v):
        if v is not None and not validate_mileage(v):
            raise InvalidMileageException()
        return v
    
    @validator('brand')
    def validate_brand(cls, v):
        if v is not None:
            iranian_brands = get_iranian_car_brands()
            if v not in iranian_brands:
                raise ValueError("برند خودرو نامعتبر است")
        return v


class VehicleOut(VehicleCreate):
    """
    Schema for vehicle output with additional fields.
    """
    id: str = Field(..., description="شناسه خودرو")
    user_id: str = Field(..., description="شناسه کاربر مالک")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")
