from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Location information
    location = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    state = Column(String(50))
    district = Column(String(50))
    
    # Weather parameters
    temperature = Column(Float)  # in Celsius
    humidity = Column(Float)  # percentage
    wind_speed = Column(Float)  # km/h
    wind_direction = Column(String(10))
    pressure = Column(Float)  # hPa
    visibility = Column(Float)  # km
    
    # Precipitation
    rainfall = Column(Float)  # mm
    rainfall_probability = Column(Float)  # percentage
    
    # Agricultural specific
    soil_moisture = Column(Float)  # percentage
    evapotranspiration = Column(Float)  # mm/day
    heat_index = Column(Float)
    
    # Forecast data
    forecast_days = Column(Integer, default=7)
    forecast_data = Column(JSON)  # Detailed forecast for multiple days
    
    # Alerts and warnings
    weather_alerts = Column(JSON)  # Any weather warnings
    agricultural_alerts = Column(JSON)  # Crop-specific warnings
    
    # Data source
    data_source = Column(String(50))  # IMD, OpenWeatherMap, etc.
    data_quality = Column(String(20))  # high, medium, low
    
    # Timestamps
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    forecast_for = Column(DateTime(timezone=True))  # When this forecast is for
    
    def __repr__(self):
        return f"<WeatherData(id={self.id}, location='{self.location}', temp={self.temperature}°C)>" 