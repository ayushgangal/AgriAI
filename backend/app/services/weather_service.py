import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching and processing weather data"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.WEATHER_BASE_URL
        self.imd_url = settings.IMD_BASE_URL
    
    async def get_current_weather(
        self, 
        latitude: float, 
        longitude: float
    ) -> Dict[str, Any]:
        """Get current weather data for a location"""
        try:
            # Try OpenWeatherMap first
            if self.api_key:
                weather_data = await self._get_openweather_data(latitude, longitude)
                if weather_data:
                    return weather_data
            
            # Fallback to IMD data
            weather_data = await self._get_imd_data(latitude, longitude)
            return weather_data
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return self._get_default_weather_data()
    
    async def get_weather_forecast(
        self, 
        latitude: float, 
        longitude: float, 
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast for a location"""
        try:
            if self.api_key:
                forecast_data = await self._get_openweather_forecast(latitude, longitude, days)
                if forecast_data:
                    return forecast_data
            
            # Fallback to IMD forecast
            forecast_data = await self._get_imd_forecast(latitude, longitude, days)
            return forecast_data
            
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {str(e)}")
            return self._get_default_forecast_data()
    
    async def get_agricultural_alerts(
        self, 
        latitude: float, 
        longitude: float
    ) -> Dict[str, Any]:
        """Get agricultural weather alerts and warnings"""
        try:
            # Get current weather
            current_weather = await self.get_current_weather(latitude, longitude)
            
            # Analyze for agricultural alerts
            alerts = self._analyze_agricultural_alerts(current_weather)
            
            return {
                "alerts": alerts,
                "weather_data": current_weather,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting agricultural alerts: {str(e)}")
            return {"alerts": [], "error": "Unable to fetch alerts"}
    
    async def _get_openweather_data(
        self, 
        latitude: float, 
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """Get weather data from OpenWeatherMap API"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/weather"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                return {
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_direction": data["wind"]["deg"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                    "rainfall": data.get("rain", {}).get("1h", 0),
                    "data_source": "OpenWeatherMap",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error fetching OpenWeatherMap data: {str(e)}")
            return None
    
    async def _get_openweather_forecast(
        self, 
        latitude: float, 
        longitude: float, 
        days: int
    ) -> Optional[Dict[str, Any]]:
        """Get weather forecast from OpenWeatherMap API"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/forecast"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": days * 8  # 8 forecasts per day
                }
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Process forecast data
                daily_forecasts = []
                for item in data["list"]:
                    daily_forecasts.append({
                        "date": item["dt_txt"],
                        "temperature": item["main"]["temp"],
                        "humidity": item["main"]["humidity"],
                        "description": item["weather"][0]["description"],
                        "rainfall": item.get("rain", {}).get("3h", 0)
                    })
                
                return {
                    "forecasts": daily_forecasts,
                    "data_source": "OpenWeatherMap",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error fetching OpenWeatherMap forecast: {str(e)}")
            return None
    
    async def _get_imd_data(
        self, 
        latitude: float, 
        longitude: float
    ) -> Dict[str, Any]:
        """Get weather data from IMD (Indian Meteorological Department)"""
        # This would integrate with IMD's API or web scraping
        # For now, return mock data
        return {
            "temperature": 28.5,
            "humidity": 65,
            "pressure": 1013,
            "wind_speed": 12,
            "wind_direction": 180,
            "description": "Partly cloudy",
            "rainfall": 0,
            "data_source": "IMD",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_imd_forecast(
        self, 
        latitude: float, 
        longitude: float, 
        days: int
    ) -> Dict[str, Any]:
        """Get weather forecast from IMD"""
        # Mock IMD forecast data
        forecasts = []
        for i in range(days):
            forecasts.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temperature": 28 + (i * 0.5),
                "humidity": 65 - (i * 2),
                "description": "Partly cloudy",
                "rainfall": 0 if i % 3 != 0 else 5
            })
        
        return {
            "forecasts": forecasts,
            "data_source": "IMD",
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_agricultural_alerts(self, weather_data: Dict[str, Any]) -> list:
        """Analyze weather data for agricultural alerts"""
        alerts = []
        
        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        rainfall = weather_data.get("rainfall", 0)
        
        # Temperature alerts
        if temperature > 35:
            alerts.append({
                "type": "high_temperature",
                "severity": "warning",
                "message": "High temperature may affect crop growth. Consider irrigation.",
                "recommendation": "Increase irrigation frequency and provide shade if possible."
            })
        elif temperature < 10:
            alerts.append({
                "type": "low_temperature",
                "severity": "warning",
                "message": "Low temperature may damage crops.",
                "recommendation": "Protect crops with covers and avoid irrigation during cold periods."
            })
        
        # Humidity alerts
        if humidity > 80:
            alerts.append({
                "type": "high_humidity",
                "severity": "info",
                "message": "High humidity may promote disease development.",
                "recommendation": "Monitor crops for disease symptoms and ensure proper ventilation."
            })
        
        # Rainfall alerts
        if rainfall > 20:
            alerts.append({
                "type": "heavy_rainfall",
                "severity": "warning",
                "message": "Heavy rainfall may cause waterlogging.",
                "recommendation": "Ensure proper drainage and avoid field operations."
            })
        
        return alerts
    
    def _get_default_weather_data(self) -> Dict[str, Any]:
        """Return default weather data when API calls fail"""
        return {
            "temperature": 25.0,
            "humidity": 60,
            "pressure": 1013,
            "wind_speed": 10,
            "wind_direction": 180,
            "description": "Partly cloudy",
            "rainfall": 0,
            "data_source": "default",
            "timestamp": datetime.now().isoformat(),
            "note": "Using default weather data due to API unavailability"
        }
    
    def _get_default_forecast_data(self) -> Dict[str, Any]:
        """Return default forecast data when API calls fail"""
        forecasts = []
        for i in range(7):
            forecasts.append({
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temperature": 25 + (i * 0.5),
                "humidity": 60 - (i * 1),
                "description": "Partly cloudy",
                "rainfall": 0
            })
        
        return {
            "forecasts": forecasts,
            "data_source": "default",
            "timestamp": datetime.now().isoformat(),
            "note": "Using default forecast data due to API unavailability"
        } 