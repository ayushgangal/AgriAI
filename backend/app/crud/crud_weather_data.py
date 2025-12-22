from sqlalchemy.orm import Session
from app.models.weather_data import WeatherData
from app.schemas.weather_data import WeatherDataCreate

class CRUDWeatherData:
    def create_weather_data(self, db: Session, *, weather_in: WeatherDataCreate):
        db_weather = WeatherData(**weather_in.dict())
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
        return db_weather

weather_data = CRUDWeatherData()
