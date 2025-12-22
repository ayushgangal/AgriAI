import logging
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.crud_crop_data import crop_data
from app.models.crop_data import CropData

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class CropService:
    def __init__(self, db: Session):
        self.db = db
        self.crop_database = self._load_crop_database()

    def _load_crop_database(self) -> Dict[str, CropData]:
        """Loads crop data from the real SQL database."""
        logger.info("Loading crop data from the database...")
        all_crops = crop_data.get_all_crops(self.db)
        return {crop.crop_name.lower(): crop for crop in all_crops}

    # ------------------------------------------------------------------
    # 1. REAL WEATHER FETCHING (Your original feature)
    # ------------------------------------------------------------------
    async def get_live_weather(self, lat: float, lon: float) -> Optional[Dict[str, float]]:
        """Fetches live weather data for the given coordinates."""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            logger.warning("OPENWEATHER_API_KEY not found in .env! Using default weather.")
            return None

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric" # Returns Temp in Celsius
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Fetched live weather for {lat},{lon}: {data['main']['temp']}°C")
                    return {
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "rainfall": 0  # OpenWeather free tier default
                    }
                else:
                    logger.error(f"Weather API Error: {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Failed to fetch weather: {e}")
            return None

    # ------------------------------------------------------------------
    # 2. CROP RECOMMENDATIONS (Your original logic)
    # ------------------------------------------------------------------
    async def get_crop_recommendations(
        self,
        weather_data: Dict[str, Any],
        latitude: float = None,
        longitude: float = None
    ) -> Dict[str, Any]:
        
        print(f"\n[DEBUG] --- STARTING RECOMMENDATION PIPELINE ---")
        
        # 1. Try to fetch LIVE weather if coordinates exist
        if latitude is not None and longitude is not None:
            live_weather = await self.get_live_weather(latitude, longitude)
            if live_weather:
                weather_data.update(live_weather)
                print(f"[DEBUG] Updated with Live Weather: {live_weather}")

        temperature = weather_data.get("temperature", 25)
        rainfall = weather_data.get("rainfall", 0)
        current_season = self._get_current_season()
        
        recommendations = []
        
        for crop_name, crop in self.crop_database.items():
            score = self._calculate_crop_suitability(
                crop, temperature, rainfall, current_season
            )

            if score > 0.3:  
                recommendations.append({
                    "crop": crop.crop_name, # Original Case
                    "scientific_name": crop.scientific_name,
                    "category": crop.crop_category,
                    "suitability_score": round(score, 2),
                    "season": crop.growing_season,
                    "reason": f"Matches temp {temperature:.1f}°C"
                })
        
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return {
            "recommendations": recommendations,
            "current_season": current_season,
            "weather_used": weather_data,
            "location": {"lat": latitude, "lon": longitude}
        }

    def _get_current_season(self) -> str:
        current_month = datetime.now().month
        if 6 <= current_month <= 10: return "kharif"
        elif current_month in [11, 12, 1, 2, 3]: return "rabi"
        else: return "zaid"

    def _calculate_crop_suitability(self, crop, temp, rain, season):
        score = 0.0
        # Temp Score
        if crop.optimal_temperature_min <= temp <= crop.optimal_temperature_max:
            score += 0.4
        elif abs(temp - crop.optimal_temperature_min) < 5:
            score += 0.2
            
        # Rain Score
        if crop.optimal_rainfall_min <= rain <= crop.optimal_rainfall_max:
            score += 0.3
        
        # Season Score
        if crop.growing_season.lower() == season or crop.growing_season.lower() == "year_round":
            score += 0.3
            
        return score

    async def get_crop_info(self, crop_name: str) -> Dict[str, Any]:
        crop = self.crop_database.get(crop_name.lower())
        if not crop:
            return {"error": "Crop not found"}
        return {
            "name": crop.crop_name,
            "category": crop.crop_category,
            "season": crop.growing_season
        }

    # ------------------------------------------------------------------
    # 3. MANAGEMENT ADVICE (The fix for your Frontend error)
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # 2. MANAGEMENT ADVICE (UPDATED - SMART LOGIC)
    # ------------------------------------------------------------------
    async def get_crop_management_advice(
        self, 
        crop_name: str, 
        growth_stage: str, 
        weather_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        # Normalize inputs
        c_name = crop_name.lower().strip()
        stage = growth_stage.lower().strip()
        
        # Extract Weather
        temp = weather_data.get("temperature", 25)
        rain = weather_data.get("rainfall", 0)
        humidity = weather_data.get("humidity", 60)

        logger.info(f"Generating advice for {c_name} at {stage} stage (T:{temp}, R:{rain}, H:{humidity})")

        # --- SMART ADVICE DATABASE ---
        # This dictionary holds specific advice for every crop and stage
        advice_db = {
            "wheat": {
                "seedling": {
                    "irrigation": "Apply light irrigation (CRI stage) 21 days after sowing. Avoid waterlogging.",
                    "nutrients": "Focus on Phosphorus for root development. Apply half dose of Nitrogen.",
                    "disease": "Monitor for termites and cutworms. Low disease risk at this stage."
                },
                "vegetative": {
                    "irrigation": "Maintain steady moisture. Irrigate every 10-12 days if no rain.",
                    "nutrients": "Top dress with remaining Nitrogen (Urea) to boost tillering.",
                    "disease": "Check for early signs of Yellow Rust (yellow stripes on leaves)."
                },
                "flowering": {
                    "irrigation": "CRITICAL STAGE: Water stress now will reduce yield significantly. Irrigate immediately.",
                    "nutrients": "Spray 2% Urea solution if leaves show yellowing. No heavy soil fertilizers.",
                    "disease": "High risk of Karnal Bunt. Apply preventative fungicide if humidity is high."
                },
                "fruiting": { # Grain Filling
                    "irrigation": "Keep soil moist but avoid heavy irrigation on windy days to prevent lodging.",
                    "nutrients": "Potash application can help improve grain weight and quality.",
                    "disease": "Watch for loose smut. Remove infected plants manually."
                },
                "maturity": {
                    "irrigation": "Stop irrigation completely to allow grain hardening.",
                    "nutrients": "No fertilizers needed.",
                    "disease": "Protect from birds and rodents. Prepare for harvest."
                }
            },
            "sugarcane": {
                "seedling": { # Germination
                    "irrigation": "Keep soil constantly moist. Irrigate every 7-10 days.",
                    "nutrients": "Basal application of NPK is required.",
                    "disease": "Dip setts in fungicide before planting to prevent Red Rot."
                },
                "vegetative": { # Tillering / Grand Growth
                    "irrigation": "High water demand. Irrigate every 7 days. This is the main growth phase.",
                    "nutrients": "High Nitrogen requirement. Apply Urea in splits.",
                    "disease": "Watch for Shoot Borer. Remove 'dead hearts' (dried shoots)."
                },
                "maturity": {
                    "irrigation": "Reduce water 1 month before harvest to increase sugar content.",
                    "nutrients": "Stop Nitrogen to prevent late vegetative growth.",
                    "disease": "Watch for Wilt. Harvest timely to prevent weight loss."
                }
            },
            "rice": {
                "seedling": {
                    "irrigation": "Maintain saturated soil but avoid deep standing water.",
                    "nutrients": "Apply DAP or SSP as basal dose.",
                    "disease": "Monitor for Blast disease spots on young leaves."
                },
                "vegetative": {
                    "irrigation": "Maintain 2-3 cm water level. Drain field for 1-2 days to aerate roots.",
                    "nutrients": "Apply Urea in splits. Zinc application is beneficial.",
                    "disease": "Watch for Stem Borer and Leaf Folder."
                },
                "flowering": {
                    "irrigation": "Keep 5cm standing water. Critical for grain formation.",
                    "nutrients": "No nitrogen at this stage. Spray Boron/Potash.",
                    "disease": "High risk of False Smut if humidity is high."
                }
            }
        }

        # --- RETRIEVE BASE ADVICE ---
        # 1. Get Crop Data (Default to empty dict if crop not found)
        crop_data = advice_db.get(c_name, {})
        
        # 2. Get Stage Data (Default to generic fallback if stage not found)
        stage_data = crop_data.get(stage, {
            "irrigation": f"Maintain standard irrigation for {c_name}.",
            "nutrients": "Standard NPK application.",
            "disease": "Monitor crop health regularly."
        })

        # --- APPLY WEATHER MODIFIERS (The AI Touch) ---
        irrigation_text = stage_data["irrigation"]
        disease_text = stage_data["disease"]

        # Rain Logic
        if rain > 5:
            irrigation_text += " **(Action: Skip irrigation due to recent rainfall.)**"
        elif rain > 20:
             irrigation_text = " **(Action: Ensure drainage to prevent waterlogging.)**"

        # Temperature Logic
        if temp > 35:
            irrigation_text += " **(Action: Increase frequency due to heat stress.)**"
        
        # Humidity/Disease Logic
        if humidity > 85:
            disease_text += " **(Warning: High humidity detects high fungal risk.)**"

        # --- RETURN RESPONSE ---
        return {
            "crop": crop_name,
            "stage": growth_stage,
            "weather_context": f"{temp}°C, {humidity}% humidity",
            
            # Send keys in all formats to guarantee Frontend works
            "irrigation_advice": irrigation_text,
            "nutrient_advice": stage_data["nutrients"],
            "disease_risk": disease_text,

            "irrigationAdvice": irrigation_text,
            "nutrientAdvice": stage_data["nutrients"],
            "diseaseRisk": disease_text,

            "data": {
                "irrigation": irrigation_text,
                "nutrients": stage_data["nutrients"],
                "disease": disease_text
            }
        }