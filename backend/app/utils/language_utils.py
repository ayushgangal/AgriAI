import logging
from typing import Dict, Set

from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SCHEMES, transliterate

# --- Configuration Constants ---

logger = logging.getLogger(__name__)

INDIC_LANGUAGES: Set[str] = {'hi', 'ta', 'te', 'bn', 'mr', 'gu', 'kn', 'ml', 'pa'}

LANGUAGE_NAMES: Dict[str, str] = {
    "en": "English", "hi": "Hindi", "ta": "Tamil", "te": "Telugu",
    "bn": "Bengali", "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada",
    "ml": "Malayalam", "pa": "Punjabi",
}

SCRIPT_MAPPING: Dict[str, str] = {
    'hi': 'devanagari', 'ta': 'tamil', 'te': 'telugu', 'bn': 'bengali',
    'mr': 'devanagari', 'gu': 'gujarati', 'kn': 'kannada', 'ml': 'malayalam',
    'pa': 'gurmukhi',
}

# --- Core Functions ---

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text between languages using GoogleTranslator.
    """
    if not text or source_lang == target_lang:
        return text
        
    try:
        # Create a translator instance and perform translation
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        logger.error(f"Translation error from '{source_lang}' to '{target_lang}': {e}")
        return text

def detect_language(text: str) -> str:
    """
    Detect the language of a given text.
    Returns 'en' (English) as a fallback.
    """
    if not text:
        return "en"

    try:
        # deep-translator's detect method returns a list like ['en', 'english']
        detected_lang_code, _ = GoogleTranslator(source='auto', target='en').detect(text)
        return detected_lang_code
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return "en"

def transliterate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Transliterate text between Indic scripts.
    """
    try:
        source_script = SCRIPT_MAPPING.get(source_lang, source_lang)
        target_script = SCRIPT_MAPPING.get(target_lang, target_lang)
        
        if source_script in SCHEMES and target_script in SCHEMES:
            return transliterate(text, source_script, target_script)
        return text
            
    except Exception as e:
        logger.error(f"Transliteration error: {e}")
        return text

# --- Utility Functions ---

def get_language_name(lang_code: str) -> str:
    """Get the human-readable name for a language code."""
    return LANGUAGE_NAMES.get(lang_code, lang_code.capitalize())

def is_indic_language(lang_code: str) -> bool:
    """Check if a language is in the defined set of Indic languages."""
    return lang_code in INDIC_LANGUAGES

def normalize_text(text: str, language: str) -> str:
    """
    Normalize text by trimming whitespace and lowercasing for English.
    """
    try:
        # Remove extra whitespace
        normalized_text = ' '.join(text.split())
        
        # Convert to lowercase only for English
        if language == 'en':
            normalized_text = normalized_text.lower()
            
        return normalized_text
    except Exception as e:
        logger.error(f"Text normalization error: {e}")
        return text
