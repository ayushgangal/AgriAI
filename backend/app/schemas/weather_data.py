from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Shared properties
class WeatherDataBase(BaseModel):
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    weather_condition: str

# Properties to receive on creation
class WeatherDataCreate(WeatherDataBase):
    pass

# Properties to return to client
class WeatherData(WeatherDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
