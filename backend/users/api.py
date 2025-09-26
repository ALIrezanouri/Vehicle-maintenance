"""
User API router for FastAPI MashinMan project.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .models import User, UserCreate, UserUpdate, UserOut, Token
from .service import UserService
from .dependencies import get_current_active_user
from core.security import create_access_token, create_refresh_token
from core.config import get_settings

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()
_settings = get_settings()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    user = await UserService.create_user(user_data)
    
    # Create tokens
    access_token_expires = timedelta(minutes=_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id), "phone": user.phone},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"user_id": str(user.id), "phone": user.phone}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login_user(phone: str, password: str):
    """Authenticate user and return JWT tokens"""
    user = await UserService.authenticate_user(phone, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await user.save()
    
    # Create tokens
    access_token_expires = timedelta(minutes=_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id), "phone": user.phone},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"user_id": str(user.id), "phone": user.phone}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    # Filter out None values
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    updated_user = await UserService.update_user(current_user.id, update_data)
    return updated_user


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: str, current_user: User = Depends(get_current_active_user)):
    """Get user by ID"""
    user = await UserService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user