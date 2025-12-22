import logging
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.crop_data import CropData
from app.crud.crud_crop_data import crop_data

logger = logging.getLogger(__name__)

class CropAPIService:
    """
    Service for fetching crop data from external APIs and databases.
    Integrates with multiple sources to provide comprehensive crop information.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AgriAI-Hackathon/1.0 (Educational Project)'
        })
    
    async def fetch_crops_from_plantnet_api(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch crop data from PlantNet API using real API key
        Note: Currently using mock data due to API endpoint issues
        """
        try:
            # PlantNet API configuration
            api_key = "2b10nNH1NQjSRx5ToTvNSEAV"
            base_url = "https://my.plantnet.org/api/v2"
            
            # Common agricultural crops to search for
            crops_to_search = [
                "tomato", "potato", "corn", "wheat", "rice", "soybean", 
                "cotton", "sugarcane", "peanut", "sunflower", "canola",
                "barley", "oats", "sorghum", "alfalfa", "chickpea",
                "lentil", "mustard", "groundnut", "onion", "carrot",
                "cabbage", "cauliflower", "pepper", "cucumber", "pumpkin"
            ]
            
            plantnet_crops = []
            
            # Try real API first, fallback to mock data if it fails
            try:
                for crop in crops_to_search[:limit]:
                    try:
                        # Search for plants by name
                        search_url = f"{base_url}/species"
                        params = {
                            "q": crop,
                            "api-key": api_key,
                            "limit": 5
                        }
                        
                        response = self.session.get(search_url, params=params, timeout=15)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if data.get("results"):
                            for result in data["results"]:
                                # Convert PlantNet data to our crop format
                                crop_data = self._convert_plantnet_to_crop_format(result, crop)
                                if crop_data:
                                    plantnet_crops.append(crop_data)
                                    break  # Only take the first result per crop to avoid duplicates
                        
                        # Add a small delay to respect rate limits
                        import asyncio
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"Error fetching {crop} from PlantNet API: {e}")
                        continue
                
                if plantnet_crops:
                    logger.info(f"Successfully fetched {len(plantnet_crops)} crops from PlantNet API")
                    return plantnet_crops
                    
            except Exception as e:
                logger.warning(f"PlantNet API failed, using mock data: {e}")
            
            # Fallback to mock data with realistic PlantNet structure
            logger.info("Using mock PlantNet data due to API issues")
            mock_plantnet_data = [
                {
                    "species": {
                        "id": "plantnet_001",
                        "scientificNameWithoutAuthor": "Solanum lycopersicum",
                        "genus": {
                            "scientificNameWithoutAuthor": "Solanum"
                        },
                        "family": {
                            "scientificNameWithoutAuthor": "Solanaceae"
                        },
                        "commonNames": [
                            {"name": "Tomato"},
                            {"name": "Love Apple"}
                        ]
                    },
                    "images": [{"url": "mock_url_1"}, {"url": "mock_url_2"}]
                },
                {
                    "species": {
                        "id": "plantnet_002",
                        "scientificNameWithoutAuthor": "Solanum tuberosum",
                        "genus": {
                            "scientificNameWithoutAuthor": "Solanum"
                        },
                        "family": {
                            "scientificNameWithoutAuthor": "Solanaceae"
                        },
                        "commonNames": [
                            {"name": "Potato"},
                            {"name": "Irish Potato"}
                        ]
                    },
                    "images": [{"url": "mock_url_3"}]
                },
                {
                    "species": {
                        "id": "plantnet_003",
                        "scientificNameWithoutAuthor": "Zea mays",
                        "genus": {
                            "scientificNameWithoutAuthor": "Zea"
                        },
                        "family": {
                            "scientificNameWithoutAuthor": "Poaceae"
                        },
                        "commonNames": [
                            {"name": "Corn"},
                            {"name": "Maize"}
                        ]
                    },
                    "images": [{"url": "mock_url_4"}]
                }
            ]
            
            # Convert mock data to crop format
            for i, mock_result in enumerate(mock_plantnet_data[:limit]):
                crop_name = crops_to_search[i] if i < len(crops_to_search) else "unknown"
                crop_data = self._convert_plantnet_to_crop_format(mock_result, crop_name)
                if crop_data:
                    plantnet_crops.append(crop_data)
            
            logger.info(f"Generated {len(plantnet_crops)} crops from mock PlantNet data")
            return plantnet_crops
            
        except Exception as e:
            logger.error(f"Error in PlantNet API service: {e}")
            return []

    async def fetch_crops_from_usda_api(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch crop data from USDA API (free and public)
        """
        try:
            # USDA API endpoint for plants database
            url = "https://plants.usda.gov/api/plants/search"
            
            # Common agricultural crops to search for
            crops_to_search = [
                "corn", "soybean", "wheat", "cotton", "alfalfa", "barley", 
                "oats", "sorghum", "sunflower", "canola", "peanut", "sugarbeet"
            ]
            
            usda_crops = []
            
            for crop in crops_to_search[:limit//len(crops_to_search)]:
                try:
                    params = {
                        "q": crop,
                        "limit": 5,
                        "offset": 0
                    }
                    
                    response = self.session.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if data.get("data"):
                        for plant in data["data"]:
                            # Convert USDA data to our format
                            crop_data = self._convert_usda_to_crop_format(plant, crop)
                            if crop_data:
                                usda_crops.append(crop_data)
                                
                except Exception as e:
                    logger.warning(f"Error fetching {crop} from USDA: {e}")
                    continue
            
            return usda_crops
            
        except Exception as e:
            logger.error(f"Error fetching from USDA API: {e}")
            return []

    def _convert_plantnet_to_crop_format(self, plantnet_result: Dict, crop_name: str) -> Optional[Dict[str, Any]]:
        """Convert PlantNet API result to our crop format"""
        try:
            # Extract basic information from PlantNet result
            species = plantnet_result.get("species", {})
            genus = species.get("genus", {})
            family = species.get("family", {})
            
            # Get scientific name
            scientific_name = f"{genus.get('scientificNameWithoutAuthor', '')} {species.get('scientificNameWithoutAuthor', '')}".strip()
            if not scientific_name:
                scientific_name = species.get("scientificNameWithoutAuthor", "")
            
            # Get common names
            common_names = []
            if species.get("commonNames"):
                common_names = [name.get("name", "") for name in species.get("commonNames", [])]
            
            # Determine crop category based on family and genus
            crop_category = self._determine_crop_category_from_plantnet(family.get("scientificNameWithoutAuthor", ""), 
                                                                       genus.get("scientificNameWithoutAuthor", ""))
            
            # Get default growing conditions for the crop
            growing_conditions = self._get_default_growing_conditions(crop_name)
            
            return {
                "crop_name": crop_name,
                "crop_variety": common_names[0] if common_names else crop_name.title(),
                "scientific_name": scientific_name,
                "crop_category": crop_category,
                "optimal_temperature_min": growing_conditions["temp_min"],
                "optimal_temperature_max": growing_conditions["temp_max"],
                "optimal_rainfall_min": growing_conditions["rain_min"],
                "optimal_rainfall_max": growing_conditions["rain_max"],
                "soil_type_preference": growing_conditions["soil_types"],
                "ph_range": growing_conditions["ph_range"],
                "growing_season": growing_conditions["season"],
                "irrigation_schedule": growing_conditions["irrigation"],
                "fertilizer_recommendations": growing_conditions["fertilizer"],
                "common_diseases": growing_conditions["diseases"],
                "common_pests": growing_conditions["pests"],
                "data_source": "plantnet_api",
                "plantnet_info": {
                    "family": family.get("scientificNameWithoutAuthor", ""),
                    "genus": genus.get("scientificNameWithoutAuthor", ""),
                    "common_names": common_names,
                    "plantnet_id": species.get("id", ""),
                    "images_count": len(plantnet_result.get("images", []))
                }
            }
        except Exception as e:
            logger.error(f"Error converting PlantNet data: {e}")
            return None

    def _convert_usda_to_crop_format(self, usda_plant: Dict, crop_name: str) -> Optional[Dict[str, Any]]:
        """Convert USDA plant data to our crop format"""
        try:
            # Default values for agricultural crops
            default_ranges = {
                "corn": {"temp_min": 18, "temp_max": 32, "rain_min": 800, "rain_max": 1500},
                "soybean": {"temp_min": 20, "temp_max": 30, "rain_min": 600, "rain_max": 1200},
                "wheat": {"temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000},
                "cotton": {"temp_min": 20, "temp_max": 35, "rain_min": 600, "rain_max": 1200},
                "alfalfa": {"temp_min": 15, "temp_max": 30, "rain_min": 400, "rain_max": 800},
                "barley": {"temp_min": 12, "temp_max": 22, "rain_min": 400, "rain_max": 800},
                "oats": {"temp_min": 10, "temp_max": 20, "rain_min": 500, "rain_max": 1000},
                "sorghum": {"temp_min": 20, "temp_max": 35, "rain_min": 400, "rain_max": 800},
                "sunflower": {"temp_min": 18, "temp_max": 30, "rain_min": 500, "rain_max": 1000},
                "canola": {"temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000},
                "peanut": {"temp_min": 20, "temp_max": 35, "rain_min": 600, "rain_max": 1200},
                "sugarbeet": {"temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000}
            }
            
            ranges = default_ranges.get(crop_name, {"temp_min": 20, "temp_max": 30, "rain_min": 600, "rain_max": 1200})
            
            return {
                "crop_name": crop_name,
                "crop_variety": usda_plant.get("commonNames", [crop_name.title()])[0] if usda_plant.get("commonNames") else crop_name.title(),
                "scientific_name": usda_plant.get("scientificName", ""),
                "crop_category": self._determine_crop_category(crop_name),
                "optimal_temperature_min": ranges["temp_min"],
                "optimal_temperature_max": ranges["temp_max"],
                "optimal_rainfall_min": ranges["rain_min"],
                "optimal_rainfall_max": ranges["rain_max"],
                "soil_type_preference": ["loamy", "clay_loam"],
                "ph_range": {"min": 6.0, "max": 7.5},
                "growing_season": self._determine_growing_season(crop_name),
                "irrigation_schedule": "drip_irrigation",
                "fertilizer_recommendations": "120:60:60 kg/ha NPK",
                "common_diseases": self._get_default_diseases(crop_name),
                "common_pests": self._get_default_pests(crop_name),
                "data_source": "usda_api"
            }
        except Exception as e:
            logger.error(f"Error converting USDA data: {e}")
            return None

    def _determine_crop_category_from_plantnet(self, family: str, genus: str) -> str:
        """Determine crop category based on PlantNet family and genus information"""
        family_lower = family.lower()
        genus_lower = genus.lower()
        
        # Vegetable families
        if any(veg_family in family_lower for veg_family in ["solanaceae", "brassicaceae", "apiaceae", "cucurbitaceae", "alliaceae"]):
            return "vegetable"
        
        # Cereal families
        if any(cereal_family in family_lower for cereal_family in ["poaceae", "gramineae"]):
            return "cereal"
        
        # Pulse families
        if any(pulse_family in family_lower for pulse_family in ["fabaceae", "leguminosae"]):
            # Check if it's a pulse or oilseed based on genus
            if any(pulse_genus in genus_lower for pulse_genus in ["cicer", "lens", "vigna", "phaseolus"]):
                return "pulse"
            else:
                return "oilseed"
        
        # Oilseed families
        if any(oil_family in family_lower for oil_family in ["asteraceae", "brassicaceae"]):
            return "oilseed"
        
        # Fiber crops
        if "malvaceae" in family_lower:
            return "fiber"
        
        # Cash crops
        if any(cash_family in family_lower for cash_family in ["amaranthaceae", "chenopodiaceae"]):
            return "cash_crop"
        
        return "other"

    def _get_default_growing_conditions(self, crop_name: str) -> Dict[str, Any]:
        """Get default growing conditions for a crop"""
        # Comprehensive growing conditions database
        conditions = {
            "tomato": {
                "temp_min": 18, "temp_max": 30, "rain_min": 600, "rain_max": 1200,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "year_round", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["early_blight", "late_blight"],
                "pests": ["aphids", "whiteflies"]
            },
            "potato": {
                "temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 5.5, "max": 6.5},
                "season": "rabi", "irrigation": "furrow_irrigation",
                "fertilizer": "120:60:60 kg/ha NPK", "diseases": ["late_blight", "bacterial_wilt"],
                "pests": ["colorado_potato_beetle", "aphids"]
            },
            "corn": {
                "temp_min": 18, "temp_max": 32, "rain_min": 800, "rain_max": 1500,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 5.5, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "120:60:60 kg/ha NPK", "diseases": ["downy_mildew", "leaf_blight"],
                "pests": ["corn_borer", "armyworm"]
            },
            "wheat": {
                "temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "sprinkler_irrigation",
                "fertilizer": "150:75:75 kg/ha NPK", "diseases": ["rust", "smut"],
                "pests": ["aphids", "army_worm"]
            },
            "rice": {
                "temp_min": 20, "temp_max": 35, "rain_min": 1500, "rain_max": 3000,
                "soil_types": ["clay", "clay_loam"], "ph_range": {"min": 5.5, "max": 7.5},
                "season": "kharif", "irrigation": "flood_irrigation",
                "fertilizer": "120:60:60 kg/ha NPK", "diseases": ["blast", "bacterial_blight"],
                "pests": ["stem_borer", "leaf_folder"]
            },
            "soybean": {
                "temp_min": 20, "temp_max": 30, "rain_min": 600, "rain_max": 1200,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "20:40:20 kg/ha NPK", "diseases": ["bacterial_blight", "root_rot"],
                "pests": ["aphids", "bean_beetle"]
            },
            "cotton": {
                "temp_min": 20, "temp_max": 35, "rain_min": 600, "rain_max": 1200,
                "soil_types": ["black_soil", "clay_loam"], "ph_range": {"min": 6.0, "max": 8.0},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "100:50:50 kg/ha NPK", "diseases": ["bacterial_blight", "leaf_curl"],
                "pests": ["boll_worm", "jassids"]
            },
            "sugarcane": {
                "temp_min": 25, "temp_max": 38, "rain_min": 1500, "rain_max": 3000,
                "soil_types": ["clay_loam", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "year_round", "irrigation": "furrow_irrigation",
                "fertilizer": "200:100:100 kg/ha NPK", "diseases": ["red_rot", "smut"],
                "pests": ["top_borer", "internode_borer"]
            },
            "peanut": {
                "temp_min": 20, "temp_max": 35, "rain_min": 600, "rain_max": 1200,
                "soil_types": ["sandy_loam", "loamy"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "20:40:20 kg/ha NPK", "diseases": ["leaf_spot", "rust"],
                "pests": ["aphids", "thrips"]
            },
            "sunflower": {
                "temp_min": 18, "temp_max": 30, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "60:30:30 kg/ha NPK", "diseases": ["downy_mildew", "rust"],
                "pests": ["sunflower_moth", "aphids"]
            },
            "canola": {
                "temp_min": 15, "temp_max": 25, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "sprinkler_irrigation",
                "fertilizer": "60:30:30 kg/ha NPK", "diseases": ["white_rust", "alternaria_blight"],
                "pests": ["aphids", "painted_bug"]
            },
            "barley": {
                "temp_min": 12, "temp_max": 22, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "sprinkler_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["rust", "smut"],
                "pests": ["aphids", "army_worm"]
            },
            "oats": {
                "temp_min": 10, "temp_max": 20, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "sprinkler_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["rust", "crown_rust"],
                "pests": ["aphids", "army_worm"]
            },
            "sorghum": {
                "temp_min": 20, "temp_max": 35, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["downy_mildew", "anthracnose"],
                "pests": ["shoot_fly", "stem_borer"]
            },
            "alfalfa": {
                "temp_min": 15, "temp_max": 30, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.5, "max": 7.5},
                "season": "year_round", "irrigation": "sprinkler_irrigation",
                "fertilizer": "20:40:20 kg/ha NPK", "diseases": ["bacterial_wilt", "anthracnose"],
                "pests": ["aphids", "weevils"]
            },
            "chickpea": {
                "temp_min": 20, "temp_max": 30, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "20:40:20 kg/ha NPK", "diseases": ["wilt", "blight"],
                "pests": ["pod_borer", "aphids"]
            },
            "lentil": {
                "temp_min": 18, "temp_max": 28, "rain_min": 300, "rain_max": 600,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "15:30:15 kg/ha NPK", "diseases": ["wilt", "root_rot"],
                "pests": ["aphids", "pod_borer"]
            },
            "mustard": {
                "temp_min": 15, "temp_max": 25, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "rabi", "irrigation": "sprinkler_irrigation",
                "fertilizer": "60:30:30 kg/ha NPK", "diseases": ["white_rust", "alternaria_blight"],
                "pests": ["aphids", "painted_bug"]
            },
            "groundnut": {
                "temp_min": 20, "temp_max": 35, "rain_min": 600, "rain_max": 1200,
                "soil_types": ["sandy_loam", "loamy"], "ph_range": {"min": 6.0, "max": 7.5},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "20:40:20 kg/ha NPK", "diseases": ["leaf_spot", "rust"],
                "pests": ["aphids", "thrips"]
            },
            "onion": {
                "temp_min": 15, "temp_max": 25, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "60:30:30 kg/ha NPK", "diseases": ["purple_blotch", "downy_mildew"],
                "pests": ["thrips", "onion_fly"]
            },
            "carrot": {
                "temp_min": 15, "temp_max": 25, "rain_min": 400, "rain_max": 800,
                "soil_types": ["sandy_loam", "loamy"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "60:30:30 kg/ha NPK", "diseases": ["leaf_blight", "root_rot"],
                "pests": ["carrot_rust_fly", "aphids"]
            },
            "cabbage": {
                "temp_min": 15, "temp_max": 25, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["black_rot", "downy_mildew"],
                "pests": ["diamondback_moth", "aphids"]
            },
            "cauliflower": {
                "temp_min": 15, "temp_max": 25, "rain_min": 400, "rain_max": 800,
                "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "rabi", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["black_rot", "downy_mildew"],
                "pests": ["diamondback_moth", "aphids"]
            },
            "pepper": {
                "temp_min": 20, "temp_max": 30, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "year_round", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["bacterial_spot", "anthracnose"],
                "pests": ["aphids", "thrips"]
            },
            "cucumber": {
                "temp_min": 20, "temp_max": 30, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "year_round", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["downy_mildew", "powdery_mildew"],
                "pests": ["cucumber_beetle", "aphids"]
            },
            "pumpkin": {
                "temp_min": 20, "temp_max": 30, "rain_min": 500, "rain_max": 1000,
                "soil_types": ["loamy", "sandy_loam"], "ph_range": {"min": 6.0, "max": 7.0},
                "season": "kharif", "irrigation": "drip_irrigation",
                "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["powdery_mildew", "downy_mildew"],
                "pests": ["squash_bug", "cucumber_beetle"]
            }
        }
        
        # Return default conditions if crop not found
        default_conditions = {
            "temp_min": 20, "temp_max": 30, "rain_min": 600, "rain_max": 1200,
            "soil_types": ["loamy", "clay_loam"], "ph_range": {"min": 6.0, "max": 7.5},
            "season": "year_round", "irrigation": "drip_irrigation",
            "fertilizer": "80:40:40 kg/ha NPK", "diseases": ["general_diseases"],
            "pests": ["general_pests"]
        }
        
        return conditions.get(crop_name, default_conditions)

    def _determine_crop_category(self, crop_name: str) -> str:
        """Determine crop category based on crop name"""
        categories = {
            "corn": "cereal",
            "wheat": "cereal", 
            "barley": "cereal",
            "oats": "cereal",
            "sorghum": "cereal",
            "soybean": "oilseed",
            "sunflower": "oilseed",
            "canola": "oilseed",
            "peanut": "oilseed",
            "cotton": "fiber",
            "alfalfa": "forage",
            "sugarbeet": "cash_crop"
        }
        return categories.get(crop_name, "other")

    def _determine_growing_season(self, crop_name: str) -> str:
        """Determine growing season based on crop name"""
        seasons = {
            "corn": "kharif",
            "soybean": "kharif",
            "cotton": "kharif",
            "sorghum": "kharif",
            "sunflower": "kharif",
            "wheat": "rabi",
            "barley": "rabi",
            "oats": "rabi",
            "alfalfa": "year_round",
            "canola": "rabi",
            "peanut": "kharif",
            "sugarbeet": "rabi"
        }
        return seasons.get(crop_name, "year_round")

    def _get_default_diseases(self, crop_name: str) -> List[str]:
        """Get default diseases for crop"""
        diseases = {
            "corn": ["downy_mildew", "leaf_blight"],
            "wheat": ["rust", "smut"],
            "soybean": ["bacterial_blight", "root_rot"],
            "cotton": ["bacterial_blight", "leaf_curl"],
            "sunflower": ["downy_mildew", "rust"],
            "peanut": ["leaf_spot", "root_rot"]
        }
        return diseases.get(crop_name, ["general_diseases"])

    def _get_default_pests(self, crop_name: str) -> List[str]:
        """Get default pests for crop"""
        pests = {
            "corn": ["corn_borer", "armyworm"],
            "wheat": ["aphids", "army_worm"],
            "soybean": ["aphids", "bean_beetle"],
            "cotton": ["boll_worm", "jassids"],
            "sunflower": ["sunflower_moth", "aphids"],
            "peanut": ["thrips", "aphids"]
        }
        return pests.get(crop_name, ["general_pests"])

    async def fetch_crops_from_local_database(self) -> List[Dict[str, Any]]:
        """Fetch additional crops from local JSON file"""
        try:
            with open("data/crops.json", "r") as f:
                local_crops = json.load(f)
            
            # Add data source information
            for crop in local_crops:
                crop["data_source"] = "local_database"
            
            return local_crops
        except Exception as e:
            logger.error(f"Error fetching from local database: {e}")
            return []

    async def fetch_crops_from_agricultural_api(self, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch crop data from agricultural research databases
        This is a mock implementation - in production, you'd integrate with real APIs
        """
        try:
            # Mock data for additional crops
            agricultural_crops = [
                {
                    "crop_name": "chickpea",
                    "crop_variety": "Desi",
                    "scientific_name": "Cicer arietinum",
                    "crop_category": "pulse",
                    "optimal_temperature_min": 20.0,
                    "optimal_temperature_max": 30.0,
                    "optimal_rainfall_min": 400.0,
                    "optimal_rainfall_max": 800.0,
                    "soil_type_preference": ["loamy", "clay_loam"],
                    "ph_range": {"min": 6.0, "max": 7.5},
                    "growing_season": "rabi",
                    "irrigation_schedule": "drip_irrigation",
                    "fertilizer_recommendations": "20:40:20 kg/ha NPK",
                    "common_diseases": ["wilt", "blight"],
                    "common_pests": ["pod_borer", "aphids"],
                    "data_source": "agricultural_api"
                },
                {
                    "crop_name": "lentil",
                    "crop_variety": "Masoor",
                    "scientific_name": "Lens culinaris",
                    "crop_category": "pulse",
                    "optimal_temperature_min": 18.0,
                    "optimal_temperature_max": 28.0,
                    "optimal_rainfall_min": 300.0,
                    "optimal_rainfall_max": 600.0,
                    "soil_type_preference": ["loamy", "sandy_loam"],
                    "ph_range": {"min": 6.0, "max": 7.5},
                    "growing_season": "rabi",
                    "irrigation_schedule": "drip_irrigation",
                    "fertilizer_recommendations": "15:30:15 kg/ha NPK",
                    "common_diseases": ["wilt", "root_rot"],
                    "common_pests": ["aphids", "pod_borer"],
                    "data_source": "agricultural_api"
                },
                {
                    "crop_name": "mustard",
                    "crop_variety": "Yellow",
                    "scientific_name": "Brassica juncea",
                    "crop_category": "oilseed",
                    "optimal_temperature_min": 15.0,
                    "optimal_temperature_max": 25.0,
                    "optimal_rainfall_min": 400.0,
                    "optimal_rainfall_max": 800.0,
                    "soil_type_preference": ["loamy", "clay_loam"],
                    "ph_range": {"min": 6.0, "max": 7.5},
                    "growing_season": "rabi",
                    "irrigation_schedule": "sprinkler_irrigation",
                    "fertilizer_recommendations": "60:30:30 kg/ha NPK",
                    "common_diseases": ["white_rust", "alternaria_blight"],
                    "common_pests": ["aphids", "painted_bug"],
                    "data_source": "agricultural_api"
                },
                {
                    "crop_name": "groundnut",
                    "crop_variety": "Spanish",
                    "scientific_name": "Arachis hypogaea",
                    "crop_category": "oilseed",
                    "optimal_temperature_min": 20.0,
                    "optimal_temperature_max": 35.0,
                    "optimal_rainfall_min": 600.0,
                    "optimal_rainfall_max": 1200.0,
                    "soil_type_preference": ["sandy_loam", "loamy"],
                    "ph_range": {"min": 6.0, "max": 7.5},
                    "growing_season": "kharif",
                    "irrigation_schedule": "drip_irrigation",
                    "fertilizer_recommendations": "20:40:20 kg/ha NPK",
                    "common_diseases": ["leaf_spot", "rust"],
                    "common_pests": ["aphids", "thrips"],
                    "data_source": "agricultural_api"
                },
                {
                    "crop_name": "onion",
                    "crop_variety": "Red",
                    "scientific_name": "Allium cepa",
                    "crop_category": "vegetable",
                    "optimal_temperature_min": 15.0,
                    "optimal_temperature_max": 25.0,
                    "optimal_rainfall_min": 400.0,
                    "optimal_rainfall_max": 800.0,
                    "soil_type_preference": ["loamy", "sandy_loam"],
                    "ph_range": {"min": 6.0, "max": 7.0},
                    "growing_season": "rabi",
                    "irrigation_schedule": "drip_irrigation",
                    "fertilizer_recommendations": "60:30:30 kg/ha NPK",
                    "common_diseases": ["purple_blotch", "downy_mildew"],
                    "common_pests": ["thrips", "onion_fly"],
                    "data_source": "agricultural_api"
                }
            ]
            return agricultural_crops[:limit]
        except Exception as e:
            logger.error(f"Error fetching from agricultural API: {e}")
            return []

    async def get_all_crops_from_apis(self, limit_per_source: int = 20) -> List[Dict[str, Any]]:
        """
        Fetch crops from all available APIs and combine them
        """
        try:
            all_crops = []
            
            # Fetch from different sources
            sources = [
                ("local_database", self.fetch_crops_from_local_database()),
                ("usda_api", self.fetch_crops_from_usda_api(limit_per_source)),
                ("plantnet_api", self.fetch_crops_from_plantnet_api(limit_per_source)),
                ("agricultural_api", self.fetch_crops_from_agricultural_api(limit_per_source))
            ]
            
            for source_name, fetch_task in sources:
                try:
                    crops = await fetch_task
                    logger.info(f"Fetched {len(crops)} crops from {source_name}")
                    all_crops.extend(crops)
                except Exception as e:
                    logger.error(f"Error fetching from {source_name}: {e}")
                    continue
            
            # Remove duplicates based on crop_name and scientific_name
            unique_crops = self._remove_duplicate_crops(all_crops)
            
            logger.info(f"Total unique crops fetched: {len(unique_crops)}")
            return unique_crops
            
        except Exception as e:
            logger.error(f"Error fetching all crops: {e}")
            return []

    def _remove_duplicate_crops(self, crops: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate crops based on crop_name and scientific_name"""
        seen = set()
        unique_crops = []
        
        for crop in crops:
            key = (crop.get("crop_name", "").lower(), crop.get("scientific_name", "").lower())
            if key not in seen:
                seen.add(key)
                unique_crops.append(crop)
        
        return unique_crops

    async def sync_crops_to_database(self, crops: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync fetched crops to the database
        """
        try:
            added_count = 0
            updated_count = 0
            errors = []
            
            for crop_data_dict in crops:
                try:
                    # Check if crop already exists
                    existing_crop = crop_data.get_crop_by_name(self.db, crop_data_dict["crop_name"])
                    
                    if existing_crop:
                        # Update existing crop
                        updated_crop = crop_data.update_crop(self.db, existing_crop.id, crop_data_dict)
                        if updated_crop:
                            updated_count += 1
                    else:
                        # Add new crop
                        new_crop = crop_data.create_crop(self.db, crop_data_dict)
                        if new_crop:
                            added_count += 1
                            
                except Exception as e:
                    errors.append(f"Error processing {crop_data_dict.get('crop_name', 'unknown')}: {str(e)}")
                    continue
            
            return {
                "added": added_count,
                "updated": updated_count,
                "errors": errors,
                "total_processed": len(crops)
            }
            
        except Exception as e:
            logger.error(f"Error syncing crops to database: {e}")
            return {"error": str(e)}

    async def refresh_crop_database(self) -> Dict[str, Any]:
        """
        Refresh the crop database by fetching from all APIs and syncing
        """
        try:
            logger.info("Starting crop database refresh...")
            
            # Fetch all crops from APIs
            crops = await self.get_all_crops_from_apis()
            
            if not crops:
                return {"error": "No crops fetched from APIs"}
            
            # Sync to database
            sync_result = await self.sync_crops_to_database(crops)
            
            logger.info(f"Crop database refresh completed: {sync_result}")
            return sync_result
            
        except Exception as e:
            logger.error(f"Error refreshing crop database: {e}")
            return {"error": str(e)} 