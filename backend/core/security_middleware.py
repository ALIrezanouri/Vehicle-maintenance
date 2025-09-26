"""
Security middleware for the MashinMan FastAPI application.
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional
import time

from .config import get_settings
from .security import decode_token

_settings = get_settings()
security = HTTPBearer()


class SecurityMiddleware:
    """Security middleware for handling authentication and authorization"""
    
    def __init__(self):
        self.settings = get_settings()
    
    async def verify_admin_access(self, request: Request) -> bool:
        """
        Verify if the current user has admin access.
        
        Args:
            request: FastAPI Request object
            
        Returns:
            bool: True if user has admin access, False otherwise
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False
            
        try:
            # Parse bearer token
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return False
                
            # Decode token
            payload = decode_token(token)
            
            # Check if user has admin role
            # In a real implementation, you would check the user's role in the database
            # For now, we'll use a simple check based on a claim in the token
            is_admin = payload.get("is_admin", False)
            return is_admin
            
        except (jwt.PyJWTError, ValueError):
            return False
    
    async def rate_limit_check(self, request: Request) -> bool:
        """
        Check if the request exceeds rate limits.
        
        Args:
            request: FastAPI Request object
            
        Returns:
            bool: True if request is allowed, False if rate limited
        """
        # In a real implementation, you would use Redis or another store
        # to track request counts per IP or user
        # For now, we'll return True to allow all requests
        return True
    
    async def check_permissions(self, request: Request, required_permissions: list) -> bool:
        """
        Check if the current user has required permissions.
        
        Args:
            request: FastAPI Request object
            required_permissions: List of required permissions
            
        Returns:
            bool: True if user has all required permissions, False otherwise
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False
            
        try:
            # Parse bearer token
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return False
                
            # Decode token
            payload = decode_token(token)
            
            # Get user permissions from token
            # In a real implementation, you would get permissions from the database
            user_permissions = payload.get("permissions", [])
            
            # Check if user has all required permissions
            return all(permission in user_permissions for permission in required_permissions)
            
        except (jwt.PyJWTError, ValueError):
            return False


# Global security middleware instance
security_middleware = SecurityMiddleware()


def require_admin_permission():
    """
    Dependency to require admin permission for an endpoint.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # In a real implementation, you would check the request context
            # For now, we'll just call the original function
            return await func(*args, **kwargs)
        return wrapper
    return decorator


async def get_current_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current admin user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        dict: User information if admin, raises HTTPException otherwise
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id: str = payload.get("user_id")
        is_admin: bool = payload.get("is_admin", False)
        
        if not user_id or not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )
            
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )