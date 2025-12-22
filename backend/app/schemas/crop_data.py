from pydantic import BaseModel
from typing import List, Dict, Optional

# Shared properties based on your detailed model
class CropDataBase(BaseModel):
    crop_name: str
    crop_variety: Optional[str] = None
    scientific_name: Optional[str] = None
    crop_category: Optional[str] = None
    optimal_temperature_min: Optional[float] = None
    optimal_temperature_max: Optional[float] = None
    optimal_rainfall_min: Optional[float] = None
    optimal_rainfall_max: Optional[float] = None
    soil_type_preference: Optional[List[str]] = []
    ph_range: Optional[Dict[str, float]] = {}
    growing_season: Optional[str] = None
    common_diseases: Optional[List[str]] = []
    common_pests: Optional[List[str]] = []

# Properties to receive on creation
class CropDataCreate(CropDataBase):
    pass

# Properties to return to client
class CropData(CropDataBase):
    id: int

    class Config:
        orm_mode = True
