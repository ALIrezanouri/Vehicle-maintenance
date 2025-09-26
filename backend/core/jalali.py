"""
Jalali calendar utilities for the MashinMan project.
"""

from datetime import datetime, date
from typing import Union
import jdatetime


def gregorian_to_jalali(gregorian_date: Union[date, datetime]) -> jdatetime.date:
    """
    Convert Gregorian date to Jalali date.
    
    Args:
        gregorian_date: Gregorian date or datetime object
        
    Returns:
        Jalali date object
    """
    if isinstance(gregorian_date, datetime):
        return jdatetime.date.fromgregorian(
            year=gregorian_date.year,
            month=gregorian_date.month,
            day=gregorian_date.day
        )
    elif isinstance(gregorian_date, date):
        return jdatetime.date.fromgregorian(
            year=gregorian_date.year,
            month=gregorian_date.month,
            day=gregorian_date.day
        )
    else:
        raise TypeError("Input must be a date or datetime object")


def jalali_to_gregorian(jalali_date: jdatetime.date) -> date:
    """
    Convert Jalali date to Gregorian date.
    
    Args:
        jalali_date: Jalali date object
        
    Returns:
        Gregorian date object
    """
    return jalali_date.togregorian()


def jalali_now() -> jdatetime.datetime:
    """
    Get current Jalali datetime.
    
    Returns:
        Current Jalali datetime
    """
    return jdatetime.datetime.now()


def format_jalali_date(jalali_date: jdatetime.date) -> str:
    """
    Format Jalali date as string.
    
    Args:
        jalali_date: Jalali date object
        
    Returns:
        Formatted date string in YYYY/MM/DD format
    """
    return jalali_date.strftime("%Y/%m/%d")


def parse_jalali_date(date_string: str) -> jdatetime.date:
    """
    Parse Jalali date string to Jalali date object.
    
    Args:
        date_string: Date string in YYYY/MM/DD format
        
    Returns:
        Jalali date object
    """
    try:
        year, month, day = map(int, date_string.split('/'))
        return jdatetime.date(year, month, day)
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY/MM/DD")


def get_jalali_month_name(month: int) -> str:
    """
    Get Persian name of Jalali month.
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Persian month name
    """
    months = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    return months[month - 1] if 1 <= month <= 12 else ""


def get_jalali_weekday_name(weekday: int) -> str:
    """
    Get Persian name of Jalali weekday.
    
    Args:
        weekday: Weekday number (0-6, where 0 is Saturday)
        
    Returns:
        Persian weekday name
    """
    weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
    return weekdays[weekday] if 0 <= weekday <= 6 else ""