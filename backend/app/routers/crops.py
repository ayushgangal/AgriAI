from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, Dict, Any
import logging
from sqlalchemy.orm import Session

from app.services.crop_service import CropService
from app.core.database import get_db
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)

# Define the router
router = APIRouter()

@router.get("/recommendations")
async def get_crop_recommendations(
    latitude: float,
    longitude: float,
    temperature: Optional[float] = None,
    rainfall: Optional[float] = None,
    humidity: Optional[float] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Get crop recommendations based on location and real-time weather."""
    try:
        # Initialize crop service with database session
        crop_service = CropService(db)
        
        # Prepare basic weather data (Frontend inputs override defaults)
        weather_data = {
            "temperature": temperature, 
            "rainfall": rainfall or 0,
            "humidity": humidity or 60
        }
        
        # Pass LATITUDE and LONGITUDE to the service so it can fetch real weather
        recommendations = await crop_service.get_crop_recommendations(
            weather_data, 
            latitude=latitude, 
            longitude=longitude
        )
        return recommendations

    except Exception as e:
        logger.error(f"Error getting crop recommendations: {str(e)}")
        # Return a clean error message to the frontend instead of crashing
        raise HTTPException(status_code=500, detail=f"Unable to fetch crop recommendations: {str(e)}")

@router.get("/management/{crop_name}")
async def get_crop_management_advice(
    crop_name: str,
    growth_stage: str,
    latitude: float,
    longitude: float,
    temperature: Optional[float] = None,
    rainfall: Optional[float] = None,
    humidity: Optional[float] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Get management advice for a specific crop"""
    try:
        crop_service = CropService(db)
        
        weather_data = {
            "temperature": temperature or 25,
            "rainfall": rainfall or 0,
            "humidity": humidity or 60
        }
        
        advice = await crop_service.get_crop_management_advice(
            crop_name, growth_stage, weather_data
        )
        return advice
    except Exception as e:
        logger.error(f"Error getting crop management advice: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch management advice")

@router.get("/info/{crop_name}")
async def get_crop_info(
    crop_name: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Get detailed information for a specific crop"""
    try:
        crop_service = CropService(db)
        info = crop_service.get_crop_info(crop_name)
        if "error" in info:
            raise HTTPException(status_code=404, detail=info["error"])
        return info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting crop info: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch crop info")