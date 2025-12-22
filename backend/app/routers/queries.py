from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
from app.services.ai_advisor import AIAdvisorService
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.query import Query as QueryModel
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# AI advisor service will be initialized per request with database session

class QueryRequest(BaseModel):
    query_text: str
    language: str = "en"
    user_location: Optional[Dict[str, float]] = None
    user_context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    response: str
    query_type: str
    recommendations: List[Dict[str, Any]]
    data_sources: List[str]
    confidence_score: str
    language: str
    timestamp: str

@router.post("/", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Process agricultural queries and provide AI-powered responses"""
    try:
        # Initialize AI advisor service with database session
        ai_advisor = AIAdvisorService(db)
        
        # Process query with AI advisor
        response = await ai_advisor.process_query(
            query_text=request.query_text,
            user_location=request.user_location,
            user_context=request.user_context,
            language=request.language
        )
        
        # Store query in database
        query_record = QueryModel(
            query_text=request.query_text,
            query_type=response.get("query_type", "general"),
            query_language=request.language,
            response_text=response.get("response", ""),
            response_data=response.get("context_data", {}),
            confidence_score=response.get("confidence_score", "medium"),
            data_sources=response.get("data_sources", [])
        )
        
        db.add(query_record)
        db.commit()
        
        return QueryResponse(**response)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to process query")

@router.post("/voice")
async def process_voice_query(
    audio_file: UploadFile = File(...),
    language: str = Form("en-IN"),
    user_location: Optional[str] = Form(None),
    user_context: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Process voice queries"""
    try:
        # Initialize AI advisor service with database session
        ai_advisor = AIAdvisorService(db)
        
        # Read audio file
        audio_content = await audio_file.read()
        
        # Parse optional parameters
        location = None
        context = None
        
        if user_location:
            import json
            location = json.loads(user_location)
        
        if user_context:
            import json
            context = json.loads(user_context)
        
        # Process voice query
        response = await ai_advisor.process_voice_query(
            audio_file=audio_content,
            language=language
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing voice query: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to process voice query")

@router.post("/image")
async def process_image_query(
    image_file: UploadFile = File(...),
    query_text: str = Form(""),
    language: str = Form("en"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Process image-based queries (e.g., crop disease identification)"""
    try:
        # Initialize AI advisor service with database session
        ai_advisor = AIAdvisorService(db)
        
        # Read image file
        image_content = await image_file.read()
        
        # Process image query
        response = await ai_advisor.process_image_query(
            image_file=image_content,
            query_text=query_text
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing image query: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to process image query")

@router.get("/history")
async def get_query_history(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Get query history"""
    try:
        queries = db.query(QueryModel).order_by(
            QueryModel.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "queries": [
                {
                    "id": query.id,
                    "query_text": query.query_text,
                    "query_type": query.query_type,
                    "response_text": query.response_text,
                    "confidence_score": query.confidence_score,
                    "created_at": query.created_at.isoformat()
                }
                for query in queries
            ],
            "total": len(queries)
        }
        
    except Exception as e:
        logger.error(f"Error getting query history: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch query history")

@router.post("/feedback")
async def submit_query_feedback(
    query_id: int,
    rating: int,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Submit feedback for a query response"""
    try:
        query = db.query(QueryModel).filter(QueryModel.id == query_id).first()
        
        if not query:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Update query with feedback
        query.user_rating = rating
        query.user_feedback = feedback
        
        db.commit()
        
        return {"message": "Feedback submitted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to submit feedback")

@router.get("/types")
async def get_query_types(
    user = Depends(get_current_user)
):
    """Get supported query types"""
    return {
        "query_types": [
            {
                "type": "weather",
                "description": "Weather-related queries (irrigation, temperature, rainfall)",
                "examples": [
                    "When should I irrigate my crops?",
                    "What's the weather forecast for next week?",
                    "Is it going to rain today?"
                ]
            },
            {
                "type": "crop",
                "description": "Crop-related queries (selection, management, diseases)",
                "examples": [
                    "Which crop should I plant this season?",
                    "How to treat crop disease?",
                    "What fertilizer should I use?"
                ]
            },
            {
                "type": "finance",
                "description": "Financial queries (credit, subsidies, market prices)",
                "examples": [
                    "What credit schemes are available?",
                    "What are the current market prices?",
                    "How to apply for subsidies?"
                ]
            },
            {
                "type": "general",
                "description": "General agricultural advice",
                "examples": [
                    "How to improve soil health?",
                    "Best farming practices",
                    "Agricultural technology advice"
                ]
            }
        ]
    }

@router.get("/capabilities")
async def get_ai_capabilities(
    user = Depends(get_current_user)
):
    """Get AI advisor capabilities"""
    return {
        "capabilities": {
            "multi_modal": {
                "text": "Natural language text queries",
                "voice": "Voice input and output",
                "image": "Image analysis for crop disease"
            },
            "languages": [
                "English", "Hindi", "Tamil", "Telugu", "Bengali",
                "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi"
            ],
            "data_sources": [
                "Indian Meteorological Department (IMD)",
                "Ministry of Agriculture",
                "NABARD",
                "Agricultural Market Information System"
            ],
            "features": [
                "Weather forecasting and alerts",
                "Crop recommendations",
                "Financial guidance",
                "Disease identification",
                "Irrigation scheduling",
                "Market price analysis"
            ]
        }
    } 