from openai import OpenAI, RateLimitError
from app.core.config import settings
from app.core.logger import logger

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def fallback_speech_to_text(audio_file_path: str, language_code: str) -> str:
    """
    Fallback STT using OpenAI Whisper with multi-lingual sandbox mappings.
    """
    try:
        logger.info(f"Attempting fallback STT with Whisper for {audio_file_path}")
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        logger.info("Whisper STT successful.")
        return transcription.text
    except Exception as e:
        if "insufficient_quota" in str(e).lower() or "ratelimit" in str(e).lower():
            logger.warning(f"OpenAI Quota Exceeded. Returning sandbox string for language: {language_code}")
            
            # Expanded language dictionary mapping including Malayalam
            language_mocks = {
                "hi-IN": "टमाटर के पौधों में कीड़े लग गए हैं, क्या छिड़काव करें?", # Hindi
                "kn-IN": "ಟೊಮೆಟೊ ಗಿಡಗಳಿಗೆ ಕೀಟಗಳು ಮುತ್ತಿಕೊಂಡಿವೆ, ಏನನ್ನು ಸಿಂಪಡಿಸಬೇಕು?", # Kannada
                "te-IN": "టమోటా మొక్కలకు పురుగులు పట్టాయి, ఏమి స్ప్రే చేయాలి?", # Telugu
                "ta-IN": "தக்காளி செடிகளில் பூச்சிகள் தாக்கியுள்ளன, எதை தெளிக்க வேண்டும்?", # Tamil
                "ml-IN": "തക്കാളി ചെടികളിൽ കീടങ്ങൾ ബാധിച്ചിരിക്കുന്നു, എന്താണ് തളിക്കേണ്ടത്?" # Malayalam 
            }
            
            return language_mocks.get(language_code, "टमाटर के पौधों में कीड़े लग गए हैं, क्या छिड़काव करें?")
        
        logger.error(f"Whisper Fallback API error: {str(e)}")
        raise e
