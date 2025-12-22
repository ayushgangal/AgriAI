import logging
import google.generativeai as genai
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from google.api_core import exceptions

logger = logging.getLogger(__name__)

class AIAdvisorService:
    def __init__(self, db: Session = None):
        self.db = db
        self.api_key = settings.GOOGLE_API_KEY
        self.model = None

        if not self.api_key:
            logger.error("CRITICAL: GOOGLE_API_KEY is missing.")
        else:
            try:
                genai.configure(api_key=self.api_key)
                
                # ✅ FIX: Using the exact model name from your debug script
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                self.chat = self.model.start_chat(history=[])
                logger.info("AgriAI (Gemini 2.5 Flash) initialized successfully.")
            except Exception as e:
                logger.error(f"AgriAI Init Error: {e}")

    async def process_query(self, query_text: str, user_location=None, user_context=None, input_type="text", language="en"):
        
        response = {
            "query": query_text,
            "query_type": "general",
            "response": "",
            "recommendations": [],
            "data_sources": [],
            "confidence_score": "low",
            "language": language,
            "timestamp": datetime.now().isoformat()
        }

        if not self.model:
            response["response"] = "⚠️ SYSTEM ERROR: AI Model not loaded. Check terminal logs."
            return response

        try:
            # System instruction to force nice formatting
            system_prompt = (
                "You are AgriAI. Answer clearly using short paragraphs and bullet points. "
                "Use **Bold** for key terms."
            )
            full_prompt = f"{system_prompt}\n\nUser Query: {query_text}"

            ai_msg = await self.chat.send_message_async(full_prompt)
            
            response["response"] = ai_msg.text
            response["confidence_score"] = "high"
            response["data_sources"] = ["Gemini 2.5", "AgriAI Knowledge Base"]
            return response

        except exceptions.ResourceExhausted:
            response["response"] = "⏳ I am thinking too fast! Please wait 20 seconds and try again. (Preview Limit)"
            return response

        except Exception as e:
            logger.error(f"Generation Error: {e}")
            response["response"] = f"⚠️ GOOGLE ERROR: {str(e)}" 
            return response