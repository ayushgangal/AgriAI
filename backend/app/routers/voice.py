from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body, Depends
from typing import Optional
import logging
from app.services.voice_service import VoiceService
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize voice service
voice_service = VoiceService()

@router.post("/speech-to-text")
async def convert_speech_to_text(
    audio_file: UploadFile = File(...),
    language: str = Form("en-IN"),
    user = Depends(get_current_user)
):
    """Convert speech to text"""
    try:
        audio_content = await audio_file.read()
        result = await voice_service.speech_to_text(audio_content, language)
        return result
    except Exception as e:
        logger.error(f"Error in speech to text: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to convert speech to text")

@router.post("/text-to-speech")
async def convert_text_to_speech(
    text: str = Form(...),
    language: str = Form("en-IN"),
    user = Depends(get_current_user)
):
    """Convert text to speech"""
    try:
        result = await voice_service.text_to_speech(text, language)
        return result
    except Exception as e:
        logger.error(f"Error in text to speech: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to convert text to speech")

@router.post("/detect-language")
async def detect_language(
    audio_file: Optional[UploadFile] = File(None),
    text: Optional[str] = Body(None),
    user = Depends(get_current_user)
):
    """Detect the language of spoken audio or text"""
    try:
        if audio_file:
            # Audio-based language detection
            audio_content = await audio_file.read()
            result = await voice_service.detect_language(audio_content)
        elif text:
            # Text-based language detection
            result = await voice_service.detect_text_language(text)
        else:
            raise HTTPException(status_code=400, detail="Either audio_file or text must be provided")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in language detection: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to detect language")

@router.get("/languages")
async def get_supported_languages(user = Depends(get_current_user)):
    """Get list of supported languages"""
    try:
        languages = await voice_service.get_supported_languages()
        return languages
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch supported languages")

@router.post("/validate-audio")
async def validate_audio_format(audio_file: UploadFile = File(...), user = Depends(get_current_user)):
    """Validate audio file format and quality"""
    try:
        audio_content = await audio_file.read()
        result = await voice_service.validate_audio_format(audio_content)
        return result
    except Exception as e:
        logger.error(f"Error validating audio format: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to validate audio format")

@router.get("/settings")
async def get_voice_settings(user = Depends(get_current_user)):
    """Get voice processing settings and capabilities"""
    try:
        settings = await voice_service.get_voice_settings()
        return settings
    except Exception as e:
        logger.error(f"Error getting voice settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch voice settings") 