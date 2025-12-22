import logging
import speech_recognition as sr
from typing import Optional, Dict, Any
import io
import wave
import numpy as np
from app.core.config import settings

logger = logging.getLogger(__name__)

class VoiceService:
    """Service for voice processing and speech recognition"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_languages = settings.SUPPORTED_LANGUAGES
        
        # Language mapping for speech recognition
        self.language_mapping = {
            "en": "en-IN",
            "hi": "hi-IN",
            "ta": "ta-IN",
            "te": "te-IN",
            "bn": "bn-IN",
            "mr": "mr-IN",
            "gu": "gu-IN",
            "kn": "kn-IN",
            "ml": "ml-IN",
            "pa": "pa-IN"
        }
    
    async def speech_to_text(
        self,
        audio_file: bytes,
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        """Convert speech to text"""
        try:
            # Convert bytes to audio data
            audio_data = self._bytes_to_audio_data(audio_file)
            
            if audio_data is None:
                return {
                    "success": False,
                    "error": "Invalid audio format",
                    "language": language
                }
            
            # Perform speech recognition
            text = self.recognizer.recognize_google(
                audio_data,
                language=language
            )
            
            return {
                "success": True,
                "text": text,
                "transcription": text,  # For compatibility
                "language": language,
                "confidence": "high"
            }
            
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Could not understand audio",
                "language": language
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "error": f"Speech recognition service error: {str(e)}",
                "language": language
            }
        except Exception as e:
            logger.error(f"Error in speech to text: {str(e)}")
            return {
                "success": False,
                "error": "Unable to process audio",
                "language": language
            }
    
    async def text_to_speech(
        self,
        text: str,
        language: str = "en-IN"
    ) -> Dict[str, Any]:
        """Convert text to speech"""
        try:
            # This would integrate with a TTS service like Google TTS or AWS Polly
            # For now, return a placeholder response with audio data
            import base64
            
            # Create a simple audio response (silence for now)
            # In production, this would call a TTS service
            audio_data = b""  # Placeholder for actual audio data
            
            return {
                "success": True,
                "audio_data": base64.b64encode(audio_data).decode('utf-8'),
                "audio_url": None,
                "language": language,
                "duration": len(text) * 0.1,  # Rough estimate
                "text": text
            }
            
        except Exception as e:
            logger.error(f"Error in text to speech: {str(e)}")
            return {
                "success": False,
                "error": "Unable to convert text to speech",
                "language": language
            }
    
    async def detect_language(self, audio_file: bytes) -> Dict[str, Any]:
        """Detect the language of spoken audio"""
        try:
            # Try recognition with multiple languages
            detected_language = None
            confidence_scores = {}
            
            audio_data = self._bytes_to_audio_data(audio_file)
            if audio_data is None:
                return {
                    "success": False,
                    "error": "Invalid audio format",
                    "supported_languages": self.supported_languages
                }
            
            for lang_code in self.supported_languages:
                try:
                    text = self.recognizer.recognize_google(
                        audio_data,
                        language=self.language_mapping.get(lang_code, lang_code)
                    )
                    
                    # If successful, this might be the language
                    confidence_scores[lang_code] = len(text)  # Simple confidence metric
                    
                except sr.UnknownValueError:
                    confidence_scores[lang_code] = 0
                except Exception:
                    confidence_scores[lang_code] = 0
            
            # Find language with highest confidence
            if confidence_scores:
                detected_language = max(confidence_scores, key=confidence_scores.get)
            
            return {
                "success": detected_language is not None,
                "language": detected_language,
                "detected_language": detected_language,
                "confidence_scores": confidence_scores,
                "supported_languages": self.supported_languages
            }
            
        except Exception as e:
            logger.error(f"Error in language detection: {str(e)}")
            return {
                "success": False,
                "error": "Unable to detect language",
                "supported_languages": self.supported_languages
            }
    
    async def detect_text_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of text (for compatibility with frontend)"""
        try:
            # Simple language detection based on character sets
            # This is a basic implementation - in production, use a proper language detection library
            
            # Check for Hindi characters
            if any('\u0900' <= char <= '\u097F' for char in text):
                return {
                    "success": True,
                    "language": "hi-IN",
                    "detected_language": "hi-IN",
                    "confidence": "medium"
                }
            
            # Check for Tamil characters
            if any('\u0B80' <= char <= '\u0BFF' for char in text):
                return {
                    "success": True,
                    "language": "ta-IN",
                    "detected_language": "ta-IN",
                    "confidence": "medium"
                }
            
            # Check for Telugu characters
            if any('\u0C00' <= char <= '\u0C7F' for char in text):
                return {
                    "success": True,
                    "language": "te-IN",
                    "detected_language": "te-IN",
                    "confidence": "medium"
                }
            
            # Check for Bengali characters
            if any('\u0980' <= char <= '\u09FF' for char in text):
                return {
                    "success": True,
                    "language": "bn-IN",
                    "detected_language": "bn-IN",
                    "confidence": "medium"
                }
            
            # Default to English
            return {
                "success": True,
                "language": "en-IN",
                "detected_language": "en-IN",
                "confidence": "medium"
            }
            
        except Exception as e:
            logger.error(f"Error in text language detection: {str(e)}")
            return {
                "success": False,
                "error": "Unable to detect language",
                "language": "en-IN"
            }
    
    def _bytes_to_audio_data(self, audio_bytes: bytes) -> Optional[sr.AudioData]:
        """Convert bytes to AudioData object"""
        try:
            # Try to read as WAV file
            with io.BytesIO(audio_bytes) as audio_io:
                with wave.open(audio_io, 'rb') as wav_file:
                    # Get audio parameters
                    frames = wav_file.readframes(wav_file.getnframes())
                    sample_rate = wav_file.getframerate()
                    sample_width = wav_file.getsampwidth()
                    
                    # Convert to AudioData
                    audio_data = sr.AudioData(
                        frames,
                        sample_rate,
                        sample_width
                    )
                    
                    return audio_data
                    
        except Exception as e:
            logger.error(f"Error converting bytes to audio data: {str(e)}")
            return None
    
    async def get_supported_languages(self) -> Dict[str, Any]:
        """Get list of supported languages"""
        return {
            "languages": [
                {
                    "code": lang,
                    "name": self._get_language_name(lang),
                    "speech_recognition": self.language_mapping.get(lang, lang)
                }
                for lang in self.supported_languages
            ],
            "total_count": len(self.supported_languages)
        }
    
    def _get_language_name(self, lang_code: str) -> str:
        """Get human-readable language name"""
        language_names = {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam",
            "pa": "Punjabi"
        }
        return language_names.get(lang_code, lang_code)
    
    async def validate_audio_format(self, audio_file: bytes) -> Dict[str, Any]:
        """Validate audio file format and quality"""
        try:
            # Check file size
            file_size = len(audio_file)
            max_size = 10 * 1024 * 1024  # 10MB
            
            if file_size > max_size:
                return {
                    "valid": False,
                    "error": "File size too large",
                    "max_size_mb": max_size / (1024 * 1024)
                }
            
            # Try to read as WAV
            try:
                with io.BytesIO(audio_file) as audio_io:
                    with wave.open(audio_io, 'rb') as wav_file:
                        sample_rate = wav_file.getframerate()
                        channels = wav_file.getnchannels()
                        duration = wav_file.getnframes() / sample_rate
                        
                        return {
                            "valid": True,
                            "format": "WAV",
                            "sample_rate": sample_rate,
                            "channels": channels,
                            "duration_seconds": duration,
                            "file_size_mb": file_size / (1024 * 1024)
                        }
                        
            except Exception:
                return {
                    "valid": False,
                    "error": "Invalid audio format. Please use WAV format.",
                    "supported_formats": ["WAV"]
                }
                
        except Exception as e:
            logger.error(f"Error validating audio format: {str(e)}")
            return {
                "valid": False,
                "error": "Unable to validate audio format"
            }
    
    async def get_voice_settings(self) -> Dict[str, Any]:
        """Get voice processing settings and capabilities"""
        return {
            "supported_languages": self.supported_languages,
            "max_file_size_mb": 10,
            "supported_formats": ["WAV"],
            "speech_recognition": {
                "provider": "Google Speech Recognition",
                "supported_languages": list(self.language_mapping.values())
            },
            "text_to_speech": {
                "provider": "Google Text-to-Speech",
                "supported_languages": list(self.language_mapping.values())
            }
        } 