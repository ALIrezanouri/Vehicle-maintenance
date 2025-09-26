"""
Admin API router for FastAPI MashinMan project.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from users.models import User, UserOut
from vehicles.models import Vehicle
from services.models import Service
from pricing.models import CarPricing
from emergency.models import EmergencyRequest, EmergencyServiceProvider
from users.dependencies import get_current_active_user
from core.security_middleware import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard/stats")
async def get_dashboard_stats(admin_user: dict = Depends(get_current_admin_user)):
    """Get dashboard statistics for admin panel"""
    # In a real implementation, you would query the database for these stats
    stats = {
        "total_users": await User.find_all().count(),
        "total_vehicles": await Vehicle.find_all().count(),
        "total_services": await Service.find_all().count(),
        "pending_emergency_requests": await EmergencyRequest.find(
            EmergencyRequest.status == "pending"
        ).count(),
        "total_service_providers": await EmergencyServiceProvider.find_all().count(),
    }
    
    return stats


@router.get("/users", response_model=List[UserOut])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get list of all users (admin only)"""
    users = await User.find_all().skip(skip).limit(limit).to_list()
    return users


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get user by ID (admin only)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Activate a user (admin only)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    user.updated_at = datetime.utcnow()
    await user.save()
    
    return {"message": "User activated successfully"}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Deactivate a user (admin only)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    user.updated_at = datetime.utcnow()
    await user.save()
    
    return {"message": "User deactivated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete associated vehicles
    await Vehicle.find(Vehicle.user_id == user.id).delete()
    
    # Delete associated services
    # Note: In a real implementation, you might want to handle this differently
    # to maintain data integrity
    
    # Delete the user
    await user.delete()
    
    return {"message": "User deleted successfully"}


@router.get("/vehicles")
async def list_all_vehicles(
    skip: int = 0,
    limit: int = 100,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get list of all vehicles (admin only)"""
    vehicles = await Vehicle.find_all().skip(skip).limit(limit).to_list()
    
    # Convert dates to Jalali for response
    from core.jalali import gregorian_to_jalali
    vehicles_out = []
    for vehicle in vehicles:
        vehicle_dict = vehicle.dict()
        if vehicle.last_service_date:
            jalali_date = gregorian_to_jalali(vehicle.last_service_date)
            vehicle_dict['last_service_date'] = jalali_date.strftime("%Y/%m/%d")
        vehicles_out.append(vehicle_dict)
    
    return vehicles_out


@router.get("/services")
async def list_all_services(
    skip: int = 0,
    limit: int = 100,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get list of all services (admin only)"""
    services = await Service.find_all().skip(skip).limit(limit).to_list()
    
    # Convert dates to Jalali for response
    from core.jalali import gregorian_to_jalali
    services_out = []
    for service in services:
        service_dict = service.dict()
        if service.last_service_date:
            jalali_date = gregorian_to_jalali(service.last_service_date)
            service_dict['last_service_date'] = jalali_date.strftime("%Y/%m/%d")
        if service.next_service_date:
            jalali_date = gregorian_to_jalali(service.next_service_date)
            service_dict['next_service_date'] = jalali_date.strftime("%Y/%m/%d")
        services_out.append(service_dict)
    
    return services_out


@router.get("/emergency-requests")
async def list_all_emergency_requests(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get list of all emergency requests (admin only)"""
    query = EmergencyRequest.find_all()
    
    if status:
        query = EmergencyRequest.find(EmergencyRequest.status == status)
    
    requests = await query.skip(skip).limit(limit).sort(-EmergencyRequest.created_at).to_list()
    
    return requests


@router.get("/service-providers")
async def list_service_providers(
    skip: int = 0,
    limit: int = 100,
    admin_user: dict = Depends(get_current_admin_user)
):
    """Get list of all service providers (admin only)"""
    providers = await EmergencyServiceProvider.find_all().skip(skip).limit(limit).to_list()
    return providers


@router.post("/pricing/bulk-update")
async def bulk_update_pricing(
    pricing_data: List[dict],
    admin_user: dict = Depends(get_current_admin_user)
):
    """Bulk update car pricing data (admin only)"""
    updated_count = 0
    
    for data in pricing_data:
        # Check if record already exists
        existing_record = await CarPricing.find_one(
            CarPricing.brand == data['brand'],
            CarPricing.model == data['model'],
            CarPricing.year == data['year'],
            CarPricing.month == data['month']
        )
        
        if existing_record:
            # Update existing record
            for key, value in data.items():
                if hasattr(existing_record, key):
                    setattr(existing_record, key, value)
            existing_record.updated_at = datetime.utcnow()
            await existing_record.save()
        else:
            # Create new record
            new_record = CarPricing(**data)
            new_record.created_at = datetime.utcnow()
            new_record.updated_at = datetime.utcnow()
            await new_record.insert()
        
        updated_count += 1
    
    return {
        "message": f"Successfully updated {updated_count} pricing records",
        "updated_count": updated_count
    }