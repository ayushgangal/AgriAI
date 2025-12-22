from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "AgriAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AgriAI - Agricultural Advisor"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./agriai.db"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    PREDICTION_SERVICE_URL: str = "http://localhost:8081/predict"

    # Market settings
    MARKET_API_URL: str = "https://api.marketdata.example.com/v1/"
    MARKET_API_KEY: Optional[str] = "your_secret_api_key_here"
    
    # AI/ML settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    MAX_TOKENS: int = 2000
    
    # Weather API settings
    OPENWEATHER_API_KEY: Optional[str] = None
    WEATHER_BASE_URL: str = "http://api.openweathermap.org/data/2.5"
    
    # Agricultural data sources
    IMD_BASE_URL: str = "https://mausam.imd.gov.in"
    AGRICULTURE_GOV_IN: str = "https://agriculture.gov.in"
    NABARD_BASE_URL: str = "https://www.nabard.org"
    
    # Voice processing
    SPEECH_RECOGNITION_LANGUAGE: str = "en-IN"
    SUPPORTED_LANGUAGES: list = ["en", "hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa"]
    
    # Caching
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Offline mode settings
    OFFLINE_MODE: bool = False
    OFFLINE_DATA_PATH: str = "data/offline"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OFFLINE_DATA_PATH, exist_ok=True) 
