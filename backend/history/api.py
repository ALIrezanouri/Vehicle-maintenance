"""
History API router for FastAPI MashinMan project.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from .models import ServiceHistory, ServiceHistoryCreate, ServiceHistoryUpdate, ServiceHistoryOut
from vehicles.models import Vehicle
from services.models import Service
from users.models import User
from users.dependencies import get_current_active_user
from core.jalali import gregorian_to_jalali, jalali_to_gregorian, parse_jalali_date

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/", response_model=ServiceHistoryOut, status_code=status.HTTP_201_CREATED)
async def create_history_record(
    history_data: ServiceHistoryCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new history record"""
    # Check if user owns the vehicle
    vehicle = await Vehicle.get(history_data.vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    if vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create history for this vehicle"
        )
    
    # Check if service belongs to this vehicle
    if history_data.service_id:
        service = await Service.get(history_data.service_id)
        if not service or service.vehicle_id != vehicle.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service does not belong to this vehicle"
            )
    
    # Parse Jalali date
    try:
        jalali_date = parse_jalali_date(history_data.service_date)
        history_data.service_date_gregorian = jalali_to_gregorian(jalali_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create history record
    history = ServiceHistory(
        service_id=history_data.service_id,
        vehicle_id=history_data.vehicle_id,
        mileage=history_data.mileage,
        service_date=history_data.service_date_gregorian,
        cost=history_data.cost,
        service_center=history_data.service_center,
        notes=history_data.notes,
        receipt_image=history_data.receipt_image,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save history to database
    await history.insert()
    
    # If this is linked to a service, mark it as completed
    if history_data.service_id and service:
        service.is_completed = True
        service.last_service_mileage = history_data.mileage
        service.last_service_date = history_data.service_date_gregorian
        # Calculate next service
        service.next_service_mileage = history_data.mileage + service.interval
        await service.save()
    
    # Update vehicle mileage if this is higher
    if history_data.mileage > vehicle.current_mileage:
        vehicle.current_mileage = history_data.mileage
        vehicle.updated_at = datetime.utcnow()
        await vehicle.save()
    
    # Convert dates to Jalali for response
    history_out = ServiceHistoryOut(**history.dict())
    jalali_date = gregorian_to_jalali(history.service_date)
    history_out.service_date = jalali_date.strftime("%Y/%m/%d")
    
    return history_out


@router.get("/", response_model=List[ServiceHistoryOut])
async def list_history_records(
    vehicle_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of history records"""
    # Build query
    if vehicle_id:
        # Check if user owns this vehicle
        vehicle = await Vehicle.get(vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access history for this vehicle"
            )
        query = ServiceHistory.vehicle_id == vehicle_id
    else:
        # Get history for all user's vehicles
        vehicle_ids = [v.id async for v in Vehicle.find(Vehicle.user_id == current_user.id)]
        query = ServiceHistory.vehicle_id.in_(vehicle_ids)
    
    history_records = await ServiceHistory.find(query).sort(-ServiceHistory.service_date).skip(skip).limit(limit).to_list()
    
    # Convert dates to Jalali for response
    history_out_list = []
    for history in history_records:
        history_out = ServiceHistoryOut(**history.dict())
        jalali_date = gregorian_to_jalali(history.service_date)
        history_out.service_date = jalali_date.strftime("%Y/%m/%d")
        history_out_list.append(history_out)
    
    return history_out_list


@router.get("/{history_id}", response_model=ServiceHistoryOut)
async def get_history_record(
    history_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get history record by ID"""
    history = await ServiceHistory.get(history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History record not found"
        )
    
    # Check if user owns the vehicle for this history record
    vehicle = await Vehicle.get(history.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this history record"
        )
    
    # Convert dates to Jalali for response
    history_out = ServiceHistoryOut(**history.dict())
    jalali_date = gregorian_to_jalali(history.service_date)
    history_out.service_date = jalali_date.strftime("%Y/%m/%d")
    
    return history_out


@router.put("/{history_id}", response_model=ServiceHistoryOut)
async def update_history_record(
    history_id: str,
    history_update: ServiceHistoryUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update history record"""
    history = await ServiceHistory.get(history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History record not found"
        )
    
    # Check if user owns the vehicle for this history record
    vehicle = await Vehicle.get(history.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this history record"
        )
    
    # Update history fields
    update_data = history_update.dict(exclude_unset=True)
    
    # Handle Jalali date conversion if provided
    if 'service_date' in update_data and update_data['service_date']:
        try:
            jalali_date = parse_jalali_date(update_data['service_date'])
            gregorian_date = jalali_to_gregorian(jalali_date)
            update_data['service_date'] = gregorian_date
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Remove the Jalali date field as it's for API only
    update_data.pop('service_date', None)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(history, key) and value is not None:
            setattr(history, key, value)
    
    # Save updated history
    await history.save()
    
    # Convert dates to Jalali for response
    history_out = ServiceHistoryOut(**history.dict())
    jalali_date = gregorian_to_jalali(history.service_date)
    history_out.service_date = jalali_date.strftime("%Y/%m/%d")
    
    return history_out


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history_record(
    history_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a history record"""
    history = await ServiceHistory.get(history_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History record not found"
        )
    
    # Check if user owns the vehicle for this history record
    vehicle = await Vehicle.get(history.vehicle_id)
    if not vehicle or vehicle.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this history record"
        )
    
    # Delete history record
    await history.delete()
    
    return None


@router.get("/export", response_model=dict)
async def export_history(
    vehicle_id: Optional[str] = None,
    format: str = "pdf",
    current_user: User = Depends(get_current_active_user)
):
    """Export history records (placeholder for actual implementation)"""
    # In a real implementation, this would generate a PDF or other format
    # For now, we'll just return a placeholder response
    
    if vehicle_id:
        # Check if user owns this vehicle
        vehicle = await Vehicle.get(vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to export history for this vehicle"
            )
    
    return {
        "message": f"History export in {format} format would be generated here",
        "vehicle_id": vehicle_id,
        "format": format,
        "status": "placeholder"
    }