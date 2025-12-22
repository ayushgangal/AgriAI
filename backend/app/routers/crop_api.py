from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.services.crop_api_service import CropAPIService
from app.crud.crud_crop_data import crop_data
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/crops", tags=["crop-api"])

@router.get("/refresh", summary="Refresh crop database from external APIs")
async def refresh_crop_database(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Refresh the crop database by fetching data from multiple external APIs.
    
    This endpoint will:
    1. Fetch crops from USDA API (free and public)
    2. Fetch crops from PlantNet API (mock data for demo)
    3. Fetch crops from agricultural research databases (mock data)
    4. Combine and deduplicate all crop data
    5. Sync the data to the local database
    
    Returns:
        Dict containing the results of the refresh operation
    """
    try:
        crop_api_service = CropAPIService(db)
        result = await crop_api_service.refresh_crop_database()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "message": "Crop database refreshed successfully",
            "result": result,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing crop database: {str(e)}")

@router.get("/fetch", summary="Fetch crops from external APIs without saving")
async def fetch_crops_from_apis(
    limit_per_source: int = Query(20, description="Number of crops to fetch per API source"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Fetch crops from external APIs without saving to the database.
    
    This is useful for previewing what crops are available from external sources
    before deciding to sync them to the database.
    
    Args:
        limit_per_source: Maximum number of crops to fetch from each API source
        
    Returns:
        Dict containing the fetched crops organized by source
    """
    try:
        crop_api_service = CropAPIService(db)
        
        # Fetch from different sources
        sources = {
            "local_database": await crop_api_service.fetch_crops_from_local_database(),
            "usda_api": await crop_api_service.fetch_crops_from_usda_api(limit_per_source),
            "plantnet_api": await crop_api_service.fetch_crops_from_plantnet_api(limit_per_source),
            "agricultural_api": await crop_api_service.fetch_crops_from_agricultural_api(limit_per_source)
        }
        
        # Get all crops combined
        all_crops = await crop_api_service.get_all_crops_from_apis(limit_per_source)
        
        return {
            "sources": sources,
            "total_unique_crops": len(all_crops),
            "all_crops": all_crops,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crops: {str(e)}")

@router.get("/sources", summary="Get available crop data sources")
async def get_crop_data_sources(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get information about available crop data sources.
    
    Returns:
        Dict containing information about each data source
    """
    sources = {
        "usda_api": {
            "name": "USDA Plants Database",
            "url": "https://plants.usda.gov/api/",
            "description": "Free public API for plant information",
            "status": "available",
            "requires_auth": False,
            "rate_limit": "None specified"
        },
        "plantnet_api": {
            "name": "PlantNet API",
            "url": "https://my.plantnet.org/",
            "description": "Plant identification and information API",
            "status": "mock_data",
            "requires_auth": True,
            "rate_limit": "Free tier available"
        },
        "agricultural_api": {
            "name": "Agricultural Research Database",
            "url": "Mock implementation",
            "description": "Agricultural research and extension data",
            "status": "mock_data",
            "requires_auth": False,
            "rate_limit": "None"
        },
        "local_database": {
            "name": "Local Crop Database",
            "url": "backend/data/crops.json",
            "description": "Local JSON file with crop information",
            "status": "available",
            "requires_auth": False,
            "rate_limit": "None"
        }
    }
    
    return {
        "sources": sources,
        "total_sources": len(sources),
        "status": "success"
    }

@router.get("/categories", summary="Get crop categories available")
async def get_crop_categories(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get all crop categories available in the database.
    
    Returns:
        Dict containing crop categories and their counts
    """
    try:
        # Get all crops from database
        all_crops = crop_data.get_all_crops(db)
        
        # Count by category
        categories = {}
        for crop in all_crops:
            category = crop.crop_category
            if category not in categories:
                categories[category] = []
            categories[category].append({
                "crop_name": crop.crop_name,
                "scientific_name": crop.scientific_name,
                "variety": crop.crop_variety
            })
        
        # Convert to count format
        category_counts = {cat: len(crops) for cat, crops in categories.items()}
        
        return {
            "categories": category_counts,
            "detailed_categories": categories,
            "total_crops": len(all_crops),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting crop categories: {str(e)}")

@router.get("/search", summary="Search crops by various criteria")
async def search_crops(
    name: Optional[str] = Query(None, description="Search by crop name"),
    category: Optional[str] = Query(None, description="Filter by crop category"),
    season: Optional[str] = Query(None, description="Filter by growing season"),
    temperature_min: Optional[float] = Query(None, description="Minimum temperature requirement"),
    temperature_max: Optional[float] = Query(None, description="Maximum temperature requirement"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Search crops by various criteria.
    
    Args:
        name: Partial crop name to search for
        category: Crop category (cereal, pulse, oilseed, etc.)
        season: Growing season (kharif, rabi, zaid, year_round)
        temperature_min: Minimum temperature requirement
        temperature_max: Maximum temperature requirement
        
    Returns:
        Dict containing matching crops
    """
    try:
        all_crops = crop_data.get_all_crops(db)
        matching_crops = []
        
        for crop in all_crops:
            # Apply filters
            if name and name.lower() not in crop.crop_name.lower():
                continue
            if category and crop.crop_category != category:
                continue
            if season and crop.growing_season != season:
                continue
            if temperature_min and crop.optimal_temperature_min < temperature_min:
                continue
            if temperature_max and crop.optimal_temperature_max > temperature_max:
                continue
            
            matching_crops.append({
                "crop_name": crop.crop_name,
                "crop_variety": crop.crop_variety,
                "scientific_name": crop.scientific_name,
                "crop_category": crop.crop_category,
                "growing_season": crop.growing_season,
                "optimal_temperature_min": crop.optimal_temperature_min,
                "optimal_temperature_max": crop.optimal_temperature_max,
                "optimal_rainfall_min": crop.optimal_rainfall_min,
                "optimal_rainfall_max": crop.optimal_rainfall_max,
                "soil_type_preference": crop.soil_type_preference,
                "ph_range": crop.ph_range,
                "irrigation_schedule": crop.irrigation_schedule,
                "fertilizer_recommendations": crop.fertilizer_recommendations,
                "common_diseases": crop.common_diseases,
                "common_pests": crop.common_pests
            })
        
        return {
            "crops": matching_crops,
            "total_matches": len(matching_crops),
            "filters_applied": {
                "name": name,
                "category": category,
                "season": season,
                "temperature_min": temperature_min,
                "temperature_max": temperature_max
            },
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching crops: {str(e)}")

@router.get("/recommendations/enhanced", summary="Get enhanced crop recommendations")
async def get_enhanced_crop_recommendations(
    temperature: float = Query(..., description="Current temperature in Celsius"),
    rainfall: float = Query(..., description="Expected rainfall in mm"),
    soil_type: Optional[str] = Query(None, description="Soil type"),
    ph_level: Optional[float] = Query(None, description="Soil pH level"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get enhanced crop recommendations based on multiple factors.
    
    This endpoint provides more detailed recommendations than the basic crop service
    by considering additional factors like soil type and pH level.
    
    Args:
        temperature: Current temperature in Celsius
        rainfall: Expected rainfall in mm
        soil_type: Type of soil (optional)
        ph_level: Soil pH level (optional)
        
    Returns:
        Dict containing detailed crop recommendations
    """
    try:
        all_crops = crop_data.get_all_crops(db)
        recommendations = []
        
        for crop in all_crops:
            score = 0.0
            factors = []
            
            # Temperature suitability
            if crop.optimal_temperature_min <= temperature <= crop.optimal_temperature_max:
                score += 0.3
                factors.append("temperature_optimal")
            elif abs(temperature - crop.optimal_temperature_min) <= 5 or abs(temperature - crop.optimal_temperature_max) <= 5:
                score += 0.2
                factors.append("temperature_acceptable")
            else:
                factors.append("temperature_poor")
            
            # Rainfall suitability
            if crop.optimal_rainfall_min <= rainfall <= crop.optimal_rainfall_max:
                score += 0.3
                factors.append("rainfall_optimal")
            elif abs(rainfall - crop.optimal_rainfall_min) <= 200 or abs(rainfall - crop.optimal_rainfall_max) <= 200:
                score += 0.2
                factors.append("rainfall_acceptable")
            else:
                factors.append("rainfall_poor")
            
            # Soil type suitability
            if soil_type and crop.soil_type_preference:
                if soil_type in crop.soil_type_preference:
                    score += 0.2
                    factors.append("soil_optimal")
                else:
                    factors.append("soil_suboptimal")
            
            # pH level suitability
            if ph_level and crop.ph_range:
                if crop.ph_range.get("min", 0) <= ph_level <= crop.ph_range.get("max", 14):
                    score += 0.2
                    factors.append("ph_optimal")
                else:
                    factors.append("ph_suboptimal")
            
            # Only include crops with reasonable suitability
            if score >= 0.3:
                recommendations.append({
                    "crop": crop.crop_name,
                    "scientific_name": crop.scientific_name,
                    "category": crop.crop_category,
                    "variety": crop.crop_variety,
                    "suitability_score": round(score, 2),
                    "factors": factors,
                    "growing_season": crop.growing_season,
                    "optimal_conditions": {
                        "temperature_range": f"{crop.optimal_temperature_min}°C - {crop.optimal_temperature_max}°C",
                        "rainfall_range": f"{crop.optimal_rainfall_min}mm - {crop.optimal_rainfall_max}mm",
                        "soil_types": crop.soil_type_preference,
                        "ph_range": crop.ph_range
                    },
                    "management_info": {
                        "irrigation": crop.irrigation_schedule,
                        "fertilizer": crop.fertilizer_recommendations,
                        "diseases": crop.common_diseases,
                        "pests": crop.common_pests
                    }
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return {
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "conditions": {
                "temperature": temperature,
                "rainfall": rainfall,
                "soil_type": soil_type,
                "ph_level": ph_level
            },
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}") 