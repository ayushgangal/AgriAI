from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging
from app.services.weather_service import WeatherService
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize weather service
weather_service = WeatherService()

@router.get("/current")
async def get_current_weather(
    latitude: float,
    longitude: float,
    user = Depends(get_current_user)
):
    """Get current weather for a location"""
    try:
        weather_data = await weather_service.get_current_weather(latitude, longitude)
        return weather_data
    except Exception as e:
        logger.error(f"Error getting current weather: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch weather data")

@router.get("/forecast")
async def get_weather_forecast(
    latitude: float,
    longitude: float,
    days: int = 7,
    user = Depends(get_current_user)
):
    """Get weather forecast for a location"""
    try:
        forecast_data = await weather_service.get_weather_forecast(latitude, longitude, days)
        return forecast_data
    except Exception as e:
        logger.error(f"Error getting weather forecast: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch forecast data")

@router.get("/alerts")
async def get_agricultural_alerts(
    latitude: float,
    longitude: float,
    user = Depends(get_current_user)
):
    """Get agricultural weather alerts"""
    try:
        alerts = await weather_service.get_agricultural_alerts(latitude, longitude)
        return alerts
    except Exception as e:
        logger.error(f"Error getting agricultural alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch alerts") 
    
@router.get("/recommendations")
async def get_agricultural_recommendations(
    latitude: float,
    longitude: float,
    user = Depends(get_current_user)
):
    """Get AI-driven agricultural recommendations"""
    try:
        # This calls the new function you created in WeatherService
        recommendations = await weather_service.get_agricultural_recommendations(latitude, longitude)
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        # Return an error compatible with your frontend
        raise HTTPException(status_code=500, detail="Unable to fetch recommendations")