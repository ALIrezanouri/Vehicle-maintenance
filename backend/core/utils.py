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
        jalali_date = jdatetime.date(year, month, day)
        gregorian_date = jalali_date.togregorian()
        return gregorian_date
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Jalali date")

def gregorian_to_jalali(date_obj: date) -> dict:
    """
    Convert Gregorian date to Jalali date.
    
    Args:
        date_obj (date): Gregorian date object
        
    Returns:
        dict: Dictionary with jalali year, month, day
    """
    try:
        jalali_date = jdatetime.date.fromgregorian(date=date_obj)
        return {
            'year': jalali_date.year,
            'month': jalali_date.month,
            'day': jalali_date.day
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Gregorian date")

def format_jalali_date(jalali_date: jdatetime.date, format_type: str = 'full') -> str:
    """
    Format Jalali date for display.
    
    Args:
        jalali_date: Jalali date object
        format_type: 'full', 'short', or 'numeric'
        
    Returns:
        str: Formatted date string
    """
    if not jalali_date:
        return ''
    
    if format_type == 'full':
        return jalali_date.strftime('%A، %d %B %Y')
    elif format_type == 'short':
        return jalali_date.strftime('%d %b %Y')
    else:  # numeric
        return jalali_date.strftime('%Y/%m/%d')

def validate_iranian_phone_number(phone_number: str) -> bool:
    """
    Validate Iranian phone number format.
    
    Args:
        phone_number (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone_number:
        return False
    
    # Remove spaces, dashes, and plus signs
    phone = re.sub(r'[\s\-\+]', '', phone_number)
    
    # Iranian mobile patterns
    mobile_patterns = [
        r'^09[0-9]{9}$',  # 09xxxxxxxxx
        r'^989[0-9]{9}$',  # 989xxxxxxxxx
        r'^00989[0-9]{9}$',  # 00989xxxxxxxxx
    ]
    
    # Iranian landline patterns (area codes)
    landline_patterns = [
        r'^0[1-8][0-9]{8,9}$',  # 0xxxxxxxxxx
    ]
    
    all_patterns = mobile_patterns + landline_patterns
    
    for pattern in all_patterns:
        if re.match(pattern, phone):
            return True
    
    return False

def normalize_iranian_phone_number(phone_number: str) -> str:
    """
    Normalize Iranian phone number for storage.
    
    Args:
        phone_number (str): Phone number to normalize
        
    Returns:
        str: Normalized phone number (09xxxxxxxxx format for mobile)
    """
    if not phone_number:
        return ''
    
    # Remove spaces, dashes, and plus signs
    phone = re.sub(r'[\s\-\+]', '', phone_number)
    
    # Convert international format to local
    if phone.startswith('00989'):
        phone = '0' + phone[4:]
    elif phone.startswith('989'):
        phone = '0' + phone[2:]
    
    return phone

def calculate_service_urgency(last_service_date: date, interval_days: int, current_mileage: int, 
                            last_service_mileage: int, interval_mileage: int) -> str:
    """
    Calculate service urgency based on date and mileage.
    
    Args:
        last_service_date: Date of last service
        interval_days: Service interval in days
        current_mileage: Current vehicle mileage
        last_service_mileage: Mileage at last service
        interval_mileage: Service interval in kilometers
        
    Returns:
        str: 'normal', 'important', or 'urgent'
    """
    today = datetime.now().date()
    
    # Calculate days since last service
    days_since_service = (today - last_service_date).days
    days_ratio = days_since_service / interval_days if interval_days > 0 else 0
    
    # Calculate mileage since last service
    mileage_since_service = current_mileage - last_service_mileage
    mileage_ratio = mileage_since_service / interval_mileage if interval_mileage > 0 else 0
    
    # Use the higher ratio to determine urgency
    max_ratio = max(days_ratio, mileage_ratio)
    
    if max_ratio >= 1.0:  # Overdue
        return 'urgent'
    elif max_ratio >= 0.8:  # 80% of interval reached
        return 'important'
    else:
        return 'normal'

def calculate_next_service_date(last_service_date: date, interval_days: int) -> date:
    """
    Calculate next service date based on interval.
    
    Args:
        last_service_date: Date of last service
        interval_days: Service interval in days
        
    Returns:
        date: Next service date
    """
    from datetime import timedelta
    return last_service_date + timedelta(days=interval_days)

def calculate_next_service_mileage(last_mileage: int, service_type: str) -> int:
    """
    Calculate next service mileage based on service type.
    
    Args:
        last_mileage (int): Last service mileage
        service_type (str): Type of service
        
    Returns:
        int: Next service mileage
    """
    interval = STANDARD_SERVICE_INTERVALS.get(service_type, 5000)
    return last_mileage + interval

def validate_mileage(mileage: int) -> bool:
    """
    Validate mileage value.
    
    Args:
        mileage (int): Mileage value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Mileage should be positive and reasonable (less than 1 million km)
    return 0 <= mileage <= 1000000

def format_mileage(mileage: int) -> str:
    """
    Format mileage for display with Persian numbers and units.
    
    Args:
        mileage: Mileage in kilometers
        
    Returns:
        str: Formatted mileage string
    """
    if mileage >= 1000:
        return f"{mileage:,} کیلومتر"
    else:
        return f"{mileage} کیلومتر"

def format_persian_number(number: Union[int, float]) -> str:
    """
    Format number with Persian digits.
    
    Args:
        number (Union[int, float]): Number to format
        
    Returns:
        str: Number formatted with Persian digits
    """
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    number_str = str(number)
    for i in range(10):
        number_str = number_str.replace(english_digits[i], persian_digits[i])
        
    return number_str

def get_persian_month_name(month_number: int) -> str:
    """
    Get Persian month name by month number.
    
    Args:
        month_number (int): Month number (1-12)
        
    Returns:
        str: Persian month name
    """
    if 1 <= month_number <= 12:
        return PERSIAN_MONTHS[month_number - 1]
    return ""

def generate_service_reminder_text(service_name: str, vehicle_info: str, due_date: str) -> str:
    """
    Generate SMS text for service reminder.
    
    Args:
        service_name: Name of the service
        vehicle_info: Vehicle information (brand, model, plate)
        due_date: Due date in Persian
        
    Returns:
        str: SMS text in Persian
    """
    return f"""سلام
یادآوری سرویس {service_name} برای خودروی {vehicle_info}
تاریخ سررسید: {due_date}
ماشین‌من"""

def get_iranian_car_brands() -> list:
    """
    Get list of Iranian car brands.
    
    Returns:
        list: List of Iranian car brands
    """
    return IRANIAN_CAR_BRANDS.copy()

def get_service_types() -> list:
    """
    Get list of service types.
    
    Returns:
        list: List of service types
    """
    return SERVICE_TYPES.copy()

def validate_phone_number(phone: str) -> bool:
    """
    Validate Iranian phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^(\+98|0)?9\d{9}$'
    return bool(re.match(pattern, phone))

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        input_str (str): Input string to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not input_str:
        return ""
        
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    return sanitized.strip()

# Custom validation error for better error handling
class CustomValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Custom exceptions for specific validation errors
class InvalidLicensePlateException(CustomValidationError):
    def __init__(self, message: str = "فرمت پلاک نامعتبر است"):
        super().__init__(message)

class InvalidMileageException(CustomValidationError):
    def __init__(self, message: str = "کیلومتر نامعتبر است"):
        super().__init__(message)
