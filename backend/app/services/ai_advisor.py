from openai import OpenAI
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.weather_service import WeatherService
from app.services.crop_service import CropService
from app.services.finance_service import FinanceService
from app.services.voice_service import VoiceService
from app.utils.language_utils import translate_text, detect_language

logger = logging.getLogger(__name__)

class AIAdvisorService:
    """Core AI advisor service that handles agricultural queries"""
    
    def __init__(self, db: Session = None):
        self.weather_service = WeatherService()
        # Only initialize CropService if db is provided
        self.crop_service = CropService(db) if db else None
        self.finance_service = FinanceService()
        self.voice_service = VoiceService()
        
        # Initialize OpenAI
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Agricultural knowledge base
        self.agricultural_context = self._load_agricultural_context()
    
    def _load_agricultural_context(self) -> Dict[str, Any]:
        """Load agricultural knowledge base for grounding AI responses"""
        return {
            "crop_cycles": {
                "kharif": ["June", "July", "August", "September", "October"],
                "rabi": ["November", "December", "January", "February", "March"],
                "zaid": ["March", "April", "May", "June"]
            },
            "irrigation_types": ["drip", "sprinkler", "flood", "furrow"],
            "soil_types": ["clay", "sandy", "loamy", "silt"],
            "fertilizer_types": ["NPK", "urea", "DAP", "organic"],
            "common_crops": ["rice", "wheat", "maize", "cotton", "sugarcane", "pulses"]
        }
    
    async def process_query(
        self,
        query_text: str,
        user_location: Optional[Dict[str, float]] = None,
        user_context: Optional[Dict[str, Any]] = None,
        input_type: str = "text",
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process agricultural queries and provide comprehensive responses
        
        Args:
            query_text: User's query in natural language
            user_location: User's location (lat, lon)
            user_context: Additional user context (crops, farm size, etc.)
            input_type: Type of input (text, voice, image)
            language: Query language
            
        Returns:
            Comprehensive response with recommendations and explanations
        """
        try:
            # Detect and translate query if needed
            detected_lang = detect_language(query_text)
            if detected_lang != "en":
                query_text = translate_text(query_text, detected_lang, "en")
            
            # Classify query type
            query_type = self._classify_query(query_text)
            
            # Gather relevant data based on query type
            context_data = await self._gather_context_data(
                query_type, user_location, user_context
            )
            
            # Generate AI response
            ai_response = await self._generate_ai_response(
                query_text, query_type, context_data, language
            )
            
            # Structure the response
            response = {
                "query": query_text,
                "query_type": query_type,
                "response": ai_response["response"],
                "recommendations": ai_response.get("recommendations", []),
                "data_sources": ai_response.get("data_sources", []),
                "confidence_score": ai_response.get("confidence_score", "medium"),
                "context_data": context_data,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "error": "Unable to process your query at the moment. Please try again.",
                "query": query_text,
                "timestamp": datetime.now().isoformat()
            }
    
    def _classify_query(self, query_text: str) -> str:
        """Classify the type of agricultural query"""
        query_lower = query_text.lower()
        
        # Weather-related queries
        if any(word in query_lower for word in ["weather", "rain", "temperature", "irrigate", "irrigation"]):
            return "weather"
        
        # Crop-related queries
        elif any(word in query_lower for word in ["crop", "seed", "plant", "harvest", "yield", "disease"]):
            return "crop"
        
        # Financial queries
        elif any(word in query_lower for word in ["price", "market", "credit", "loan", "subsidy", "cost"]):
            return "finance"
        
        # General agricultural advice
        else:
            return "general"
    
    async def _gather_context_data(
        self,
        query_type: str,
        user_location: Optional[Dict[str, float]],
        user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Gather relevant data based on query type"""
        context_data = {}
        
        if user_location:
            # Get weather data
            if query_type in ["weather", "crop", "general"]:
                weather_data = await self.weather_service.get_current_weather(
                    user_location["latitude"], user_location["longitude"]
                )
                context_data["weather"] = weather_data
            
            # Get crop recommendations (only if crop_service is available)
            if query_type in ["crop", "general"] and self.crop_service:
                try:
                    crop_data = await self.crop_service.get_crop_recommendations(
                        context_data.get("weather", {})
                    )
                    context_data["crops"] = crop_data
                except Exception as e:
                    logger.warning(f"Could not get crop recommendations: {e}")
                    context_data["crops"] = {"recommendations": [], "error": "Crop service unavailable"}
            elif query_type in ["crop", "general"]:
                context_data["crops"] = {"recommendations": [], "error": "Crop service not initialized"}
        
        # Get financial data if needed
        if query_type == "finance":
            finance_data = await self.finance_service.get_financial_info(
                user_location, user_context
            )
            context_data["finance"] = finance_data
        
        return context_data
    
    async def _generate_ai_response(
        self,
        query_text: str,
        query_type: str,
        context_data: Dict[str, Any],
        language: str
    ) -> Dict[str, Any]:
        """Generate AI response using OpenAI"""
        
        # Create system prompt with agricultural context
        system_prompt = self._create_system_prompt(query_type, context_data)
        
        # Create user prompt
        user_prompt = f"""
        Query: {query_text}
        
        Please provide a comprehensive, practical response that:
        1. Addresses the specific question
        2. Provides actionable recommendations
        3. Explains the reasoning behind recommendations
        4. Considers local conditions and constraints
        5. Uses simple, understandable language
        6. Includes relevant data and sources
        
        If the response should be in a language other than English, please indicate.
        """
        
        try:
            if not self.client:
                raise ValueError("OpenAI API key not configured")
                
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse and structure the response
            structured_response = self._structure_ai_response(
                ai_response, query_type, context_data
            )
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return {
                "response": "I'm having trouble processing your request right now. Please try again later.",
                "confidence_score": "low"
            }
    
    def _create_system_prompt(self, query_type: str, context_data: Dict[str, Any]) -> str:
        """Create system prompt with agricultural context"""
        
        base_prompt = """
        You are AgriAI, an expert agricultural advisor designed to help Indian farmers make informed decisions. 
        You provide practical, actionable advice based on local conditions and best practices.
        
        Key principles:
        - Always consider local weather, soil, and market conditions
        - Provide specific, actionable recommendations
        - Explain the reasoning behind your advice
        - Consider cost-effectiveness and sustainability
        - Be aware of government schemes and subsidies
        - Use simple, understandable language
        - Be honest about limitations and uncertainties
        
        Agricultural context:
        """
        
        # Add relevant context based on query type
        if query_type == "weather":
            weather_info = context_data.get("weather", {})
            base_prompt += f"""
            Current weather conditions: {json.dumps(weather_info, indent=2)}
            Consider how weather affects irrigation, crop health, and farming activities.
            """
        
        elif query_type == "crop":
            crop_info = context_data.get("crops", {})
            base_prompt += f"""
            Crop recommendations and data: {json.dumps(crop_info, indent=2)}
            Consider soil conditions, weather, market prices, and local practices.
            """
        
        elif query_type == "finance":
            finance_info = context_data.get("finance", {})
            base_prompt += f"""
            Financial information: {json.dumps(finance_info, indent=2)}
            Consider government schemes, credit availability, and market trends.
            """
        
        return base_prompt
    
    def _structure_ai_response(
        self,
        ai_response: str,
        query_type: str,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Structure the AI response with recommendations and metadata"""
        
        # Extract recommendations and data sources
        recommendations = []
        data_sources = []
        
        # Add data sources based on context
        if "weather" in context_data:
            data_sources.append("Indian Meteorological Department (IMD)")
        if "crops" in context_data:
            data_sources.append("Ministry of Agriculture")
        if "finance" in context_data:
            data_sources.append("NABARD")
            data_sources.append("Agricultural Market Information System")
        
        return {
            "response": ai_response,
            "recommendations": recommendations,
            "data_sources": data_sources,
            "confidence_score": "high" if context_data else "medium"
        }
    
    async def process_voice_query(
        self,
        audio_file: bytes,
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        """Process voice queries"""
        try:
            # Convert speech to text
            text = await self.voice_service.speech_to_text(audio_file, language)
            
            # Process the text query
            response = await self.process_query(text, language=language)
            
            # Convert response to speech if needed
            audio_response = await self.voice_service.text_to_speech(
                response["response"], language
            )
            
            response["audio_response"] = audio_response
            return response
            
        except Exception as e:
            logger.error(f"Error processing voice query: {str(e)}")
            return {"error": "Unable to process voice query"}
    
    async def process_image_query(
        self,
        image_file: bytes,
        query_text: str = ""
    ) -> Dict[str, Any]:
        """Process image-based queries (e.g., crop disease identification)"""
        try:
            # Analyze image for crop disease or other agricultural features
            image_analysis = await self._analyze_agricultural_image(image_file)
            
            # Combine with text query
            combined_query = f"{query_text} {image_analysis['description']}"
            
            # Process the combined query
            response = await self.process_query(combined_query)
            response["image_analysis"] = image_analysis
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing image query: {str(e)}")
            return {"error": "Unable to process image query"}
    
    async def _analyze_agricultural_image(self, image_file: bytes) -> Dict[str, Any]:
        """Analyze agricultural images for disease, crop type, etc."""
        # This would integrate with computer vision models
        # For now, return a placeholder
        return {
            "description": "Image analysis not implemented yet",
            "confidence": "low",
            "detected_features": []
        } 