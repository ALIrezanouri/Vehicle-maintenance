"""
Service API router for FastAPI MashinMan project.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from .models import Service, ServiceCreate, ServiceUpdate, ServiceOut
from vehicles.models import Vehicle
from users.models import User
from users.dependencies import get_current_active_user
from core.jalali import gregorian_to_jalali, jalali_to_gregorian, parse_jalali_date

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new service"""
    # Check if user owns the vehicle
    vehicle = await Vehicle.get(service_data.vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create service for this vehicle"
        )
    
    # Parse Jalali dates if provided
    if service_data.last_service_date:
        try:
            jalali_date = parse_jalali_date(service_data.last_service_date)
            service_data.last_service_date_gregorian = jalali_to_gregorian(jalali_date)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    if service_data.next_service_date:
        try:
            jalali_date = parse_jalali_date(service_data.next_service_date)
            service_data.next_service_date_gregorian = jalali_to_gregorian(jalali_date)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Create service instance
    service = Service(
        vehicle_id=service_data.vehicle_id,
        type=service_data.type,
        name=service_data.name,
        interval=service_data.interval,
        last_service_mileage=service_data.last_service_mileage,
        last_service_date=service_data.last_service_date_gregorian,
        next_service_mileage=service_data.next_service_mileage,
        next_service_date=service_data.next_service_date_gregorian,
        urgency=service_data.urgency,
        cost=service_data.cost,
        service_center=service_data.service_center,
        notes=service_data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save service to database
    await service.insert()
    
    # Convert dates to Jalali for response
    service_out = ServiceOut(**service.dict())
    if service.last_service_date:
        jalali_date = gregorian_to_jalali(service.last_service_date)
        service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    if service.next_service_date:
        jalali_date = gregorian_to_jalali(service.next_service_date)
        service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return service_out


@router.get("/", response_model=List[ServiceOut])
async def list_services(
    vehicle_id: Optional[str] = None,
    is_completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of services"""
    # Build query
    query = Service.vehicle_id.in_(
        [v.id async for v in Vehicle.find(Vehicle.user_id == current_user.id)]
    )
    
    if vehicle_id:
        # Check if user owns this vehicle
        vehicle = await Vehicle.get(vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access services for this vehicle"
            )
        query = Service.vehicle_id == vehicle_id
    
    if is_completed is not None:
        query = query & (Service.is_completed == is_completed)
    
    services = await Service.find(query).skip(skip).limit(limit).to_list()
    
    # Convert dates to Jalali for response
    services_out = []
    for service in services:
        service_out = ServiceOut(**service.dict())
        if service.last_service_date:
            jalali_date = gregorian_to_jalali(service.last_service_date)
            service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
        
        if service.next_service_date:
            jalali_date = gregorian_to_jalali(service.next_service_date)
            service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
        
        services_out.append(service_out)
    
    return services_out


@router.get("/upcoming", response_model=List[ServiceOut])
async def get_upcoming_services(
    days: int = 30,
    current_user: User = Depends(get_current_active_user)
):
    """Get upcoming services within specified days"""
    # Calculate date range
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=days)
    
    # Build query for upcoming services
    query = (
        (Service.vehicle_id.in_(
            [v.id async for v in Vehicle.find(Vehicle.user_id == current_user.id)]
        )) &
        (Service.is_completed == False) &
        (Service.next_service_date <= end_date) &
        (Service.next_service_date >= today)
    )
    
    services = await Service.find(query).sort(Service.next_service_date).to_list()
    
    # Convert dates to Jalali for response
    services_out = []
    for service in services:
        service_out = ServiceOut(**service.dict())
        if service.last_service_date:
            jalali_date = gregorian_to_jalali(service.last_service_date)
            service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
        
        if service.next_service_date:
            jalali_date = gregorian_to_jalali(service.next_service_date)
            service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
        
        services_out.append(service_out)
    
    return services_out


@router.get("/{service_id}", response_model=ServiceOut)
async def get_service(
    service_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get service by ID"""
    service = await Service.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check if user owns the vehicle for this service
    vehicle = await Vehicle.get(service.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this service"
        )
    
    # Convert dates to Jalali for response
    service_out = ServiceOut(**service.dict())
    if service.last_service_date:
        jalali_date = gregorian_to_jalali(service.last_service_date)
        service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    if service.next_service_date:
        jalali_date = gregorian_to_jalali(service.next_service_date)
        service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return service_out


@router.put("/{service_id}", response_model=ServiceOut)
async def update_service(
    service_id: str,
    service_update: ServiceUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update service information"""
    service = await Service.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check if user owns the vehicle for this service
    vehicle = await Vehicle.get(service.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this service"
        )
    
    # Update service fields
    update_data = service_update.dict(exclude_unset=True)
    
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
    
    if 'next_service_date' in update_data and update_data['next_service_date']:
        try:
            jalali_date = parse_jalali_date(update_data['next_service_date'])
            gregorian_date = jalali_to_gregorian(jalali_date)
            update_data['next_service_date'] = gregorian_date
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Remove the Jalali date fields as they're for API only
    update_data.pop('last_service_date', None)
    update_data.pop('next_service_date', None)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(service, key) and value is not None:
            setattr(service, key, value)
    
    # Save updated service
    await service.save()
    
    # Convert dates to Jalali for response
    service_out = ServiceOut(**service.dict())
    if service.last_service_date:
        jalali_date = gregorian_to_jalali(service.last_service_date)
        service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    if service.next_service_date:
        jalali_date = gregorian_to_jalali(service.next_service_date)
        service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return service_out


@router.put("/{service_id}/complete", response_model=ServiceOut)
async def complete_service(
    service_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark service as completed"""
    service = await Service.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check if user owns the vehicle for this service
    vehicle = await Vehicle.get(service.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this service"
        )
    
    # Mark as completed
    service.is_completed = True
    service.updated_at = datetime.utcnow()
    await service.save()
    
    # Convert dates to Jalali for response
    service_out = ServiceOut(**service.dict())
    if service.last_service_date:
        jalali_date = gregorian_to_jalali(service.last_service_date)
        service_out.last_service_date = jalali_date.strftime("%Y/%m/%d")
    
    if service.next_service_date:
        jalali_date = gregorian_to_jalali(service.next_service_date)
        service_out.next_service_date = jalali_date.strftime("%Y/%m/%d")
    
    return service_out


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a service"""
    service = await Service.get(service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check if user owns the vehicle for this service
    vehicle = await Vehicle.get(service.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this service"
        )
    
    # Delete service
    await service.delete()
    
    return None