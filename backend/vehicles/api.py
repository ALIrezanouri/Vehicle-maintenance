"""
Vehicle API router for FastAPI MashinMan project.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from .models import Vehicle, VehicleCreate, VehicleUpdate, VehicleOut
from users.models import User
from users.dependencies import get_current_active_user
from core.jalali import gregorian_to_jalali, jalali_to_gregorian, parse_jalali_date

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new vehicle"""
    # Parse Jalali dates if provided
    if vehicle_data.last_service_date:
        try:
            jalali_date = parse_jalali_date(vehicle_data.last_service_date)
            gregorian_date = jalali_to_gregorian(jalali_date)
            vehicle_data.last_service_date_gregorian = gregorian_date
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Create vehicle instance
    vehicle = Vehicle(
        user_id=current_user.id,
        license_plate=vehicle_data.license_plate,
        brand=vehicle_data.brand,
        model=vehicle_data.model,
        manufacture_year=vehicle_data.manufacture_year,
        current_mileage=vehicle_data.current_mileage,
        last_service_date=vehicle_data.last_service_date_gregorian,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save vehicle to database
    await vehicle.insert()
    
    # Convert dates to Jalali for response
    vehicle_out = VehicleOut(**vehicle.dict())
    if vehicle.last_service_date:
        jalali_date = gregorian_to_jalali(vehicle.last_service_date)
        vehicle_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return vehicle_out


@router.get("/", response_model=List[VehicleOut])
async def list_vehicles(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of vehicles for current user"""
    vehicles = await Vehicle.find(
        Vehicle.user_id == current_user.id
    ).skip(skip).limit(limit).to_list()
    
    # Convert dates to Jalali for response
    vehicles_out = []
    for vehicle in vehicles:
        vehicle_out = VehicleOut(**vehicle.dict())
        if vehicle.last_service_date:
            jalali_date = gregorian_to_jalali(vehicle.last_service_date)
            vehicle_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
        vehicles_out.append(vehicle_out)
    
    return vehicles_out


@router.get("/{vehicle_id}", response_model=VehicleOut)
async def get_vehicle(
    vehicle_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get vehicle by ID"""
    vehicle = await Vehicle.get(vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check if user owns this vehicle
    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this vehicle"
        )
    
    # Convert dates to Jalali for response
    vehicle_out = VehicleOut(**vehicle.dict())
    if vehicle.last_service_date:
        jalali_date = gregorian_to_jalali(vehicle.last_service_date)
        vehicle_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return vehicle_out


@router.put("/{vehicle_id}", response_model=VehicleOut)
async def update_vehicle(
    vehicle_id: str,
    vehicle_update: VehicleUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update vehicle information"""
    vehicle = await Vehicle.get(vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check if user owns this vehicle
    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this vehicle"
        )
    
    # Update vehicle fields
    update_data = vehicle_update.dict(exclude_unset=True)
    
    # Handle Jalali date conversion if provided
    if 'last_service_date' in update_data and update_data['last_service_date']:
        try:
            jalali_date = parse_jalali_date(update_data['last_service_date'])
            gregorian_date = jalali_to_gregorian(jalali_date)
            update_data['last_service_date'] = gregorian_date
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Remove the Jalali date field as it's for API only
    update_data.pop('last_service_date', None)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(vehicle, key) and value is not None:
            setattr(vehicle, key, value)
    
    # Save updated vehicle
    await vehicle.save()
    
    # Convert dates to Jalali for response
    vehicle_out = VehicleOut(**vehicle.dict())
    if vehicle.last_service_date:
        jalali_date = gregorian_to_jalali(vehicle.last_service_date)
        vehicle_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return vehicle_out


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a vehicle"""
    vehicle = await Vehicle.get(vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check if user owns this vehicle
    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this vehicle"
        )
    
    # Delete vehicle
    await vehicle.delete()
    
    return None