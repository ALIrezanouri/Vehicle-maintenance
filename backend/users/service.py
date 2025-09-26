"""
User service for FastAPI MashinMan project.
Handles user-related business logic.
"""

from typing import Optional
from fastapi import HTTPException, status
from beanie import PydanticObjectId

from .models import User, UserCreate
from core.security import get_password_hash
from core.config import get_settings

_settings = get_settings()


class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[User]:
        """Get user by phone number"""
        return await User.find_one(User.phone == phone)
    
    @staticmethod
    async def get_user_by_id(user_id: PydanticObjectId) -> Optional[User]:
        """Get user by ID"""
        return await User.get(user_id)
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user with this phone already exists
        existing_user = await UserService.get_user_by_phone(user_data.phone)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone number already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user instance
        user = User(
            name=user_data.name,
            phone=user_data.phone,
            email=user_data.email,
            password=hashed_password,
            city=user_data.city,
            emergency_contact_name=user_data.emergency_contact_name,
            emergency_contact_phone=user_data.emergency_contact_phone,
        )
        
        # Save user to database
        await user.insert()
        return user
    
    @staticmethod
    async def authenticate_user(phone: str, password: str) -> Optional[User]:
        """Authenticate user with phone and password"""
        user = await UserService.get_user_by_phone(phone)
        if not user or not user.check_password(password):
            return None
        return user
    
    @staticmethod
    async def update_user(user_id: PydanticObjectId, update_data: dict) -> User:
        """Update user information"""
        user = await UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update user fields
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        await user.save()
        return user