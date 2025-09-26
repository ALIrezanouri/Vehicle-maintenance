"""
Custom exception handler for MashinMan project.
Provides Persian error messages and standardized error responses.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
import logging

logger = logging.getLogger('mashinman')

# Persian error messages
ERROR_MESSAGES = {
    'authentication_failed': 'احراز هویت ناموفق بود.',
    'not_authenticated': 'برای دسترسی به این بخش باید وارد شوید.',
    'permission_denied': 'شما اجازه دسترسی به این بخش را ندارید.',
    'not_found': 'آیتم مورد نظر یافت نشد.',
    'method_not_allowed': 'این عملیات مجاز نیست.',
    'validation_error': 'خطا در اعتبارسنجی داده‌ها.',
    'invalid_license_plate': 'فرمت پلاک نامعتبر است.',
    'invalid_mileage': 'کیلومتر نامعتبر است.',
    'invalid_phone': 'شماره تلفن نامعتبر است.',
    'server_error': 'خطای داخلی سرور.',
    'emergency_request_failed': 'درخواست اضطراری با خطا مواجه شد.',
    'service_already_completed': 'سرویس قبلاً تکمیل شده است.',
    'invalid_date': 'تاریخ نامعتبر است.',
    'invalid_phone_number': 'شماره تلفن نامعتبر است.',
}

async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom exception handler for FastAPI application.
    
    Args:
        request (Request): Incoming request
        exc (Exception): Raised exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    logger.exception(exc)
    
    # Handle HTTP exceptions
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": {
                    "code": "http_error",
                    "message": ERROR_MESSAGES.get(exc.detail, exc.detail),
                    "status_code": exc.status_code
                }
            }
        )
    
    # Handle validation errors
    if isinstance(exc, ValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error['loc']),
                "message": error['msg']
            })
        
        return JSONResponse(
            status_code=422,
            content={
                "detail": {
                    "code": "validation_error",
                    "message": ERROR_MESSAGES['validation_error'],
                    "errors": errors
                }
            }
        )
    
    # Handle custom HTTP exceptions
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": {
                    "code": "http_exception",
                    "message": str(exc.detail),
                    "status_code": exc.status_code
                }
            }
        )
    
    # Handle general exceptions
    return JSONResponse(
        status_code=500,
        content={
            "detail": {
                "code": "server_error",
                "message": ERROR_MESSAGES['server_error'],
                "status_code": 500
            }
        }
    )

# Custom exception classes
class InvalidLicensePlateException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['invalid_license_plate']):
        self.message = message
        super().__init__(self.message)

class InvalidMileageException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['invalid_mileage']):
        self.message = message
        super().__init__(self.message)

class InvalidPhoneException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['invalid_phone']):
        self.message = message
        super().__init__(self.message)

class EmergencyRequestFailedException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['emergency_request_failed']):
        self.message = message
        super().__init__(self.message)

class ServiceAlreadyCompletedException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['service_already_completed']):
        self.message = message
        super().__init__(self.message)

class InvalidDateException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['invalid_date']):
        self.message = message
        super().__init__(self.message)

class InvalidPhoneNumberException(Exception):
    def __init__(self, message: str = ERROR_MESSAGES['invalid_phone_number']):
        self.message = message
        super().__init__(self.message)
