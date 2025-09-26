"""
Pricing models for FastAPI MashinMan project using Beanie ODM.
"""

from typing import Optional, List
from datetime import datetime, date
from beanie import Document
from pydantic import BaseModel, Field, validator
import jdatetime
from core.utils import get_iranian_car_brands


class CarPricing(Document):
    """
    Car pricing model for storing market prices of vehicles.
    """
    
    # Vehicle identification
    brand: str = Field(..., description="برند")
    model: str = Field(..., description="مدل")
    year: int = Field(..., description="سال ساخت")
    
    # Vehicle specifications
    trim: Optional[str] = Field(None, description="تریم خودرو")
    engine_size: Optional[float] = Field(None, description="حجم موتور (سی‌سی)")
    transmission_type: Optional[str] = Field(None, description="نوع گیربکس")
    
    # Pricing information
    price: int = Field(..., description="قیمت (ریال)")
    currency: str = Field(default="IRR", description="واحد پول")
    price_date: date = Field(..., description="تاریخ قیمت")
    
    # Market information
    source: Optional[str] = Field(None, description="منبع قیمت")
    region: Optional[str] = Field(None, description="منطقه جغرافیایی")
    condition: Optional[str] = Field(None, description="وضعیت خودرو")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "car_pricings"
    
    @validator('brand')
    def validate_brand(cls, v):
        iranian_brands = get_iranian_car_brands()
        if v not in iranian_brands:
            raise ValueError("برند خودرو نامعتبر است")
        return v


class ServicePricing(Document):
    """
    Service pricing model for storing service costs.
    """
    
    # Service identification
    service_type: str = Field(..., description="نوع سرویس")
    service_name: str = Field(..., description="نام سرویس")
    
    # Pricing information
    base_price: int = Field(..., description="قیمت پایه (ریال)")
    estimated_duration: int = Field(..., description="مدت زمان تخمینی (دقیقه)")
    
    # Vehicle compatibility
    compatible_brands: List[str] = Field(default=[], description="برندهای سازگار")
    compatible_models: List[str] = Field(default=[], description="مدلهای سازگار")
    
    # Validity
    valid_from: date = Field(..., description="تاریخ شروع اعتبار")
    valid_until: Optional[date] = Field(None, description="تاریخ پایان اعتبار")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "service_pricings"


# Pydantic models for API
class CarPricingCreate(BaseModel):
    """
    Schema for creating a new car pricing record.
    """
    brand: str = Field(..., description="برند")
    model: str = Field(..., description="مدل")
    year: int = Field(..., description="سال ساخت")
    trim: Optional[str] = Field(None, description="تریم خودرو")
    engine_size: Optional[float] = Field(None, description="حجم موتور (سی‌سی)")
    transmission_type: Optional[str] = Field(None, description="نوع گیربکس")
    price: int = Field(..., description="قیمت (ریال)")
    currency: str = Field(default="IRR", description="واحد پول")
    price_date: date = Field(..., description="تاریخ قیمت")
    source: Optional[str] = Field(None, description="منبع قیمت")
    region: Optional[str] = Field(None, description="منطقه جغرافیایی")
    condition: Optional[str] = Field(None, description="وضعیت خودرو")
    
    @validator('brand')
    def validate_brand(cls, v):
        iranian_brands = get_iranian_car_brands()
        if v not in iranian_brands:
            raise ValueError("برند خودرو نامعتبر است")
        return v


class CarPricingUpdate(BaseModel):
    """
    Schema for updating a car pricing record.
    """
    brand: Optional[str] = Field(None, description="برند")
    model: Optional[str] = Field(None, description="مدل")
    year: Optional[int] = Field(None, description="سال ساخت")
    trim: Optional[str] = Field(None, description="تریم خودرو")
    engine_size: Optional[float] = Field(None, description="حجم موتور (سی‌سی)")
    transmission_type: Optional[str] = Field(None, description="نوع گیربکس")
    price: Optional[int] = Field(None, description="قیمت (ریال)")
    currency: Optional[str] = Field(None, description="واحد پول")
    price_date: Optional[date] = Field(None, description="تاریخ قیمت")
    source: Optional[str] = Field(None, description="منبع قیمت")
    region: Optional[str] = Field(None, description="منطقه جغرافیایی")
    condition: Optional[str] = Field(None, description="وضعیت خودرو")
    
    @validator('brand')
    def validate_brand(cls, v):
        if v is not None:
            iranian_brands = get_iranian_car_brands()
            if v not in iranian_brands:
                raise ValueError("برند خودرو نامعتبر است")
        return v


class CarPricingOut(CarPricingCreate):
    """
    Schema for car pricing output with additional fields.
    """
    id: str = Field(..., description="شناسه قیمت خودرو")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ به‌روزرسانی")
