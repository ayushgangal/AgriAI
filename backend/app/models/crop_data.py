from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class CropData(Base):
    __tablename__ = "crop_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Crop information
    crop_name = Column(String(100), nullable=False)
    crop_variety = Column(String(100))
    scientific_name = Column(String(100))
    crop_category = Column(String(50))  # cereal, pulse, oilseed, etc.
    
    # Growing requirements
    optimal_temperature_min = Column(Float)  # Celsius
    optimal_temperature_max = Column(Float)  # Celsius
    optimal_rainfall_min = Column(Float)  # mm
    optimal_rainfall_max = Column(Float)  # mm
    soil_type_preference = Column(JSON)  # List of preferred soil types
    ph_range = Column(JSON)  # min and max pH values
    
    # Growing cycle
    growing_season = Column(String(50))  # kharif, rabi, zaid
    sowing_time = Column(JSON)  # Recommended sowing periods
    harvesting_time = Column(JSON)  # Expected harvesting periods
    growth_duration = Column(Integer)  # days
    
    # Yield and economics
    expected_yield_min = Column(Float)  # tons/hectare
    expected_yield_max = Column(Float)  # tons/hectare
    market_price_range = Column(JSON)  # min and max prices
    cost_of_cultivation = Column(Float)  # per hectare
    
    # Disease and pest information
    common_diseases = Column(JSON)
    common_pests = Column(JSON)
    disease_management = Column(Text)
    pest_management = Column(Text)
    
    # Recommendations
    irrigation_schedule = Column(JSON)
    fertilizer_recommendations = Column(JSON)
    pesticide_recommendations = Column(JSON)
    
    # Regional data
    suitable_regions = Column(JSON)  # List of suitable states/districts
    current_season_status = Column(String(50))  # recommended, not_recommended, neutral
    
    # Data source
    data_source = Column(String(50))
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CropData(id={self.id}, crop='{self.crop_name}', variety='{self.crop_variety}')>" 