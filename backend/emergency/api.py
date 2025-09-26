"""
Emergency API router for FastAPI MashinMan project.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import math

from .models import (
    EmergencyRequest, EmergencyServiceProvider,
    EmergencyRequestCreate, EmergencyRequestUpdate, EmergencyRequestOut,
    EmergencyServiceProviderCreate, EmergencyServiceProviderUpdate, EmergencyServiceProviderOut
)
from vehicles.models import Vehicle
from users.models import User
from users.dependencies import get_current_active_user
from core.jalali import gregorian_to_jalali

router = APIRouter(prefix="/emergency", tags=["emergency"])


@router.post("/sos", response_model=EmergencyRequestOut, status_code=status.HTTP_201_CREATED)
async def create_emergency_request(
    request_data: EmergencyRequestCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create an emergency request (SOS)"""
    # If vehicle_id is provided, check if user owns this vehicle
    if request_data.vehicle_id:
        vehicle = await Vehicle.get(request_data.vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create emergency request for this vehicle"
            )
    
    # Create emergency request
    emergency_request = EmergencyRequest(
        user_id=current_user.id,
        vehicle_id=request_data.vehicle_id,
        latitude=request_data.latitude,
        longitude=request_data.longitude,
        location_address=request_data.location_address,
        description=request_data.description,
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save emergency request to database
    await emergency_request.insert()
    
    # Convert to output model
    request_out = EmergencyRequestOut(**emergency_request.dict())
    
    return request_out


@router.get("/requests", response_model=List[EmergencyRequestOut])
async def list_emergency_requests(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of emergency requests (user's own requests)"""
    # Build query for user's own requests
    query = EmergencyRequest.user_id == current_user.id
    
    if status:
        query = query & (EmergencyRequest.status == status)
    
    requests = await EmergencyRequest.find(query).sort(-EmergencyRequest.created_at).skip(skip).limit(limit).to_list()
    
    # Convert to output models
    requests_out = []
    for request in requests:
        request_out = EmergencyRequestOut(**request.dict())
        requests_out.append(request_out)
    
    return requests_out


@router.get("/requests/{request_id}", response_model=EmergencyRequestOut)
async def get_emergency_request(
    request_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get emergency request by ID"""
    request = await EmergencyRequest.get(request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency request not found"
        )
    
    # Check if user owns this request
    if request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this emergency request"
        )
    
    # Convert to output model
    request_out = EmergencyRequestOut(**request.dict())
    
    return request_out


@router.put("/requests/{request_id}", response_model=EmergencyRequestOut)
async def update_emergency_request(
    request_id: str,
    request_update: EmergencyRequestUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update emergency request"""
    request = await EmergencyRequest.get(request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency request not found"
        )
    
    # Check if user owns this request
    if request.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this emergency request"
        )
    
    # Update request fields
    update_data = request_update.dict(exclude_unset=True)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(request, key) and value is not None:
            setattr(request, key, value)
    
    # Save updated request
    await request.save()
    
    # Convert to output model
    request_out = EmergencyRequestOut(**request.dict())
    
    return request_out


@router.post("/providers", response_model=EmergencyServiceProviderOut, status_code=status.HTTP_201_CREATED)
async def create_service_provider(
    provider_data: EmergencyServiceProviderCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create an emergency service provider (admin only in production)"""
    # In a production environment, this would be restricted to admin users only
    # For now, we'll allow any authenticated user to create service providers
    
    # Create service provider
    provider = EmergencyServiceProvider(
        name=provider_data.name,
        phone=provider_data.phone,
        service_type=provider_data.service_type,
        latitude=provider_data.latitude,
        longitude=provider_data.longitude,
        service_radius=provider_data.service_radius,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save provider to database
    await provider.insert()
    
    # Convert to output model
    provider_out = EmergencyServiceProviderOut(**provider.dict())
    
    return provider_out


@router.get("/providers", response_model=List[EmergencyServiceProviderOut])
async def list_service_providers(
    service_type: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: int = 10,  # in kilometers
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of emergency service providers"""
    # Build query
    query = EmergencyServiceProvider.is_active == True
    
    if service_type:
        query = query & (EmergencyServiceProvider.service_type == service_type)
    
    providers = await EmergencyServiceProvider.find(query).skip(skip).limit(limit).to_list()
    
    # If location is provided, filter by proximity
    if latitude is not None and longitude is not None:
        nearby_providers = []
        for provider in providers:
            # Calculate distance using haversine formula
            distance = calculate_distance(latitude, longitude, provider.latitude, provider.longitude)
            if distance <= min(radius, provider.service_radius):
                nearby_providers.append(provider)
        providers = nearby_providers
    
    # Convert to output models
    providers_out = []
    for provider in providers:
        provider_out = EmergencyServiceProviderOut(**provider.dict())
        providers_out.append(provider_out)
    
    return providers_out


@router.get("/providers/{provider_id}", response_model=EmergencyServiceProviderOut)
async def get_service_provider(
    provider_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get emergency service provider by ID"""
    provider = await EmergencyServiceProvider.get(provider_id)
    if not provider or not provider.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider not found"
        )
    
    # Convert to output model
    provider_out = EmergencyServiceProviderOut(**provider.dict())
    
    return provider_out


@router.put("/providers/{provider_id}", response_model=EmergencyServiceProviderOut)
async def update_service_provider(
    provider_id: str,
    provider_update: EmergencyServiceProviderUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update emergency service provider (admin/provider owner only in production)"""
    # In a production environment, this would be restricted to admin users or provider owners
    # For now, we'll allow any authenticated user to update service providers
    
    provider = await EmergencyServiceProvider.get(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service provider not found"
        )
    
    # Update provider fields
    update_data = provider_update.dict(exclude_unset=True)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(provider, key) and value is not None:
            setattr(provider, key, value)
    
    # Save updated provider
    await provider.save()
    
    # Convert to output model
    provider_out = EmergencyServiceProviderOut(**provider.dict())
    
    return provider_out


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth
    using the haversine formula. Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r