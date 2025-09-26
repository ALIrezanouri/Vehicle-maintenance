"""
Core utilities for MashinMan project.
Includes Jalali date handling, license plate validation, and other common functions.
"""

import re
import jdatetime
from datetime import datetime, date
from typing import Union, Optional, Dict, List
from fastapi import HTTPException
from pydantic import ValidationError
from vehicles.models import LicensePlateData

# Iranian license plate patterns
LICENSE_PLATE_PATTERNS = [
    # Standard format: 123آ456
    r'^[0-9]{2,3}[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی][0-9]{3}$',
    # Alternative format: IR15-546T55
    r'^IR[0-9]{2}-[0-9]{3}[A-Z][0-9]{2}$',
    # Motorcycle format: 123456789
    r'^[0-9]{8,9}$',
    # Taxi format: T123آ456
    r'^T[0-9]{2,3}[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی][0-9]{3}$',
    # Police format: P123آ456
    r'^P[0-9]{2,3}[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی][0-9]{3}$',
]

# Persian month names for Jalali date handling
PERSIAN_MONTHS = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
]

# Iranian car brands for validation
IRANIAN_CAR_BRANDS = [
    'پراید', 'پژو', 'دنا', 'رانا', 'سمند', 'آریسان', 'آریا', 'تیبا', 
    'جک S3', 'جک S5', 'جک S7', 'جیلی Emgrand', 'جیلی GC9', 'خودرو', 
    'دی‌اول', 'رانا', 'رامیدر', 'ساینا', 'شاهین', 'کوئیک', 'موسو', 'نایرا'
]

# Standard service intervals (in kilometers)
STANDARD_SERVICE_INTERVALS = {
    'oil_change': 5000,
    'air_filter': 10000,
    'oil_filter': 10000,
    'timing_belt': 60000,
    'brake_fluid': 20000,
    'coolant': 40000,
    'spark_plug': 30000,
    'transmission_fluid': 50000,
}

# Service types
SERVICE_TYPES = [
    'oil_change', 'tire_rotation', 'brake_inspection', 'engine_tuning',
    'air_filter_replacement', 'oil_filter_replacement', 'coolant_change',
    'transmission_service', 'battery_check', 'suspension_inspection',
    'exhaust_system_check', 'electrical_system_check', 'ac_service'
]

def validate_iranian_license_plate(plate: str) -> bool:
    """
    Validate Iranian license plate format.
    
    Args:
        plate (str): License plate string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not plate:
        return False
        
    # Normalize plate (remove spaces and convert to uppercase)
    normalized_plate = plate.replace(' ', '').replace('-', '').upper()
    
    # Check against all patterns
    for pattern in LICENSE_PLATE_PATTERNS:
        if re.match(pattern, normalized_plate):
            return True
            
    return False

def normalize_license_plate(plate: str) -> str:
    """
    Normalize license plate format.
    
    Args:
        plate (str): Raw license plate string
        
    Returns:
        str: Normalized license plate
    """
    if not plate:
        return ""
        
    # Remove extra spaces and normalize
    return plate.replace(' ', '').replace('-', '').upper()

def format_license_plate_data(plate_data: LicensePlateData) -> str:
    """
    Format license plate data into a string.
    
    Args:
        plate_data (LicensePlateData): License plate data object
        
    Returns:
        str: Formatted license plate string
    """
    if not plate_data:
        return ""
    
    # Check if it's a motorcycle (no serial)
    if not plate_data.plaqueSerial:
        return f"{plate_data.plaqueLeftNo}{plate_data.plaqueMiddleChar}{plate_data.plaqueRightNo}"
    
    # Default to car plate format
    return f"{plate_data.plaqueLeftNo}{plate_data.plaqueMiddleChar}{plate_data.plaqueRightNo}-{plate_data.plaqueSerial}"

def parse_license_plate_string(plate_string: str) -> LicensePlateData:
    """
    Parse license plate string into LicensePlateData object.
    
    Args:
        plate_string (str): License plate string
        
    Returns:
        LicensePlateData: Parsed license plate data
    """
    if not plate_string:
        return LicensePlateData(
            plaqueLeftNo="",
            plaqueMiddleChar="",
            plaqueRightNo="",
            plaqueSerial=""
        )
    
    # Try to parse as car plate (format like "123ب456-78")
    car_match = re.match(r'^(\d{2})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})-(\d{2})$', plate_string)
    if car_match:
        return LicensePlateData(
            plaqueLeftNo=car_match.group(1),
            plaqueMiddleChar=car_match.group(2),
            plaqueRightNo=car_match.group(3),
            plaqueSerial=car_match.group(4)
        )
    
    # Try to parse as motorcycle plate (format like "12345678")
    motorcycle_match = re.match(r'^(\d{3})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})$', plate_string)
    if motorcycle_match:
        return LicensePlateData(
            plaqueLeftNo=motorcycle_match.group(1),
            plaqueMiddleChar=motorcycle_match.group(2),
            plaqueRightNo=motorcycle_match.group(3),
            plaqueSerial=""
        )
    
    # Default empty plate
    return LicensePlateData(
        plaqueLeftNo="",
        plaqueMiddleChar="",
        plaqueRightNo="",
        plaqueSerial=""
    )

def jalali_to_gregorian(year: int, month: int, day: int) -> date:
    """
    Convert Jalali date to Gregorian date.
    
    Args:
        year (int): Jalali year
        month (int): Jalali month
        day (int): Jalali day
        
    Returns:
        date: Gregorian date
    """
    try:
        gregorian_date = jdatetime.date(year, month, day).togregorian()
        return gregorian_date
    except ValueError:
        raise HTTPException(status_code=400, detail="تاریخ نامعتبر است")

def gregorian_to_jalali(date_obj: date) -> Dict[str, int]:
    """
    Convert Gregorian date to Jalali date.
    
    Args:
        date_obj (date): Gregorian date object
        
    Returns:
        Dict[str, int]: Jalali date as dictionary with year, month, day keys
    """
    jalali_date = jdatetime.date.fromgregorian(date=date_obj)
    return {
        "year": jalali_date.year,
        "month": jalali_date.month,
        "day": jalali_date.day
    }

def validate_mileage(mileage: int) -> bool:
    """
    Validate mileage value.
    
    Args:
        mileage (int): Mileage value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Mileage should be a positive integer not exceeding 1,000,000 km
    return isinstance(mileage, int) and 0 <= mileage <= 1000000

def get_iranian_car_brands() -> List[str]:
    """
    Get list of Iranian car brands.
    
    Returns:
        List[str]: List of Iranian car brands
    """
    return IRANIAN_CAR_BRANDS

def get_service_types() -> List[str]:
    """
    Get list of service types.
    
    Returns:
        List[str]: List of service types
    """
    return SERVICE_TYPES

def get_standard_service_intervals() -> Dict[str, int]:
    """
    Get standard service intervals.
    
    Returns:
        Dict[str, int]: Dictionary of service types and their standard intervals in kilometers
    """
    return STANDARD_SERVICE_INTERVALS

def get_persian_months() -> List[str]:
    """
    Get list of Persian months.
    
    Returns:
        List[str]: List of Persian months
    """
    return PERSIAN_MONTHS
