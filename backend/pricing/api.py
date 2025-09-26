"""
Pricing API router for FastAPI MashinMan project.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from .models import CarPricing, CarPricingCreate, CarPricingUpdate, CarPricingOut
from users.models import User
from users.dependencies import get_current_active_user
from core.jalali import gregorian_to_jalali

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/", response_model=CarPricingOut, status_code=status.HTTP_201_CREATED)
async def create_pricing_record(
    pricing_data: CarPricingCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new pricing record (admin only in production)"""
    # In a production environment, this would be restricted to admin users only
    # For now, we'll allow any authenticated user to create pricing records
    
    # Check if a record already exists for this brand/model/year/month combination
    existing_record = await CarPricing.find_one(
        CarPricing.brand == pricing_data.brand,
        CarPricing.model == pricing_data.model,
        CarPricing.year == pricing_data.year,
        CarPricing.month == pricing_data.month
    )
    
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pricing record already exists for this brand/model/year/month combination"
        )
    
    # Create pricing record
    pricing = CarPricing(
        brand=pricing_data.brand,
        model=pricing_data.model,
        year=pricing_data.year,
        month=pricing_data.month,
        price=pricing_data.price,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    # Save pricing to database
    await pricing.insert()
    
    # Convert to output model
    pricing_out = CarPricingOut(**pricing.dict())
    
    return pricing_out


@router.get("/", response_model=List[CarPricingOut])
async def list_pricing_records(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of pricing records"""
    # Build query
    query = CarPricing
    
    if brand:
        query = query.find(CarPricing.brand == brand)
    
    if model:
        query = query.find(CarPricing.model == model)
    
    if year:
        query = query.find(CarPricing.year == year)
    
    pricing_records = await query.skip(skip).limit(limit).sort(-CarPricing.year, -CarPricing.month).to_list()
    
    # Convert to output models
    pricing_out_list = []
    for pricing in pricing_records:
        pricing_out = CarPricingOut(**pricing.dict())
        pricing_out_list.append(pricing_out)
    
    return pricing_out_list


@router.get("/history", response_model=List[CarPricingOut])
async def get_pricing_history(
    brand: str,
    model: str,
    year: int,
    limit: int = 12,
    current_user: User = Depends(get_current_active_user)
):
    """Get pricing history for a specific car model"""
    pricing_records = await CarPricing.find(
        CarPricing.brand == brand,
        CarPricing.model == model,
        CarPricing.year == year
    ).sort(-CarPricing.month).limit(limit).to_list()
    
    # Convert to output models
    pricing_out_list = []
    for pricing in pricing_records:
        pricing_out = CarPricingOut(**pricing.dict())
        pricing_out_list.append(pricing_out)
    
    return pricing_out_list


@router.get("/compare", response_model=List[CarPricingOut])
async def compare_models(
    brands: str,  # comma-separated list of brands
    models: str,  # comma-separated list of models
    year: int,
    month: int,
    current_user: User = Depends(get_current_active_user)
):
    """Compare prices of different car models"""
    brand_list = brands.split(",")
    model_list = models.split(",")
    
    # Ensure we have the same number of brands and models
    if len(brand_list) != len(model_list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of brands must match number of models"
        )
    
    pricing_records = []
    for brand, model in zip(brand_list, model_list):
        pricing = await CarPricing.find_one(
            CarPricing.brand == brand.strip(),
            CarPricing.model == model.strip(),
            CarPricing.year == year,
            CarPricing.month == month
        )
        
        if pricing:
            pricing_out = CarPricingOut(**pricing.dict())
            pricing_records.append(pricing_out)
    
    return pricing_records


@router.get("/{pricing_id}", response_model=CarPricingOut)
async def get_pricing_record(
    pricing_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get pricing record by ID"""
    pricing = await CarPricing.get(pricing_id)
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing record not found"
        )
    
    # Convert to output model
    pricing_out = CarPricingOut(**pricing.dict())
    
    return pricing_out


@router.put("/{pricing_id}", response_model=CarPricingOut)
async def update_pricing_record(
    pricing_id: str,
    pricing_update: CarPricingUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update pricing record (admin only in production)"""
    # In a production environment, this would be restricted to admin users only
    # For now, we'll allow any authenticated user to update pricing records
    
    pricing = await CarPricing.get(pricing_id)
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing record not found"
        )
    
    # Update pricing fields
    update_data = pricing_update.dict(exclude_unset=True)
    
    # Update timestamps
    update_data['updated_at'] = datetime.utcnow()
    
    # Apply updates
    for key, value in update_data.items():
        if hasattr(pricing, key) and value is not None:
            setattr(pricing, key, value)
    
    # Save updated pricing
    await pricing.save()
    
    # Convert to output model
    pricing_out = CarPricingOut(**pricing.dict())
    
    return pricing_out


@router.delete("/{pricing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pricing_record(
    pricing_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a pricing record (admin only in production)"""
    # In a production environment, this would be restricted to admin users only
    # For now, we'll allow any authenticated user to delete pricing records
    
    pricing = await CarPricing.get(pricing_id)
    if not pricing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing record not found"
        )
    
    # Delete pricing record
    await pricing.delete()
    
    return None