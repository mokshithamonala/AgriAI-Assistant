from langdetect import detect, DetectorFactory
from app.core.logger import logger

# Set seed for consistent language detection
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    """
    Detects the language of the incoming text.
    Returns standard ISO 639-1 language codes (e.g., 'hi' for Hindi, 'kn' for Kannada, 'en' for English).
    """
    try:
        lang_code = detect(text)
        logger.info(f"Detected language code: {lang_code}")
        
        # Mapping langdetect codes to Sarvam/Standard expected codes if necessary
        lang_map = {
            "hi": "hi-IN",
            "kn": "kn-IN",
            "en": "en-IN"
        }
        
        return lang_map.get(lang_code, lang_code)
    except Exception as e:
        logger.warning(f"Language detection failed, defaulting to 'en-IN'. Error: {str(e)}")
        return "en-IN"