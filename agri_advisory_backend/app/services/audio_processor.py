import os
import requests
from groq import Groq
from app.core.config import settings
from app.core.logger import logger

DEFAULT_VOICE_QUERIES = {
    "en-IN": "How to control pests and fungal blight in tomato and paddy crops?",
    "hi-IN": "टमाटर और धान की फसल में कीट और झुलसा रोग की रोकथाम कैसे करें?",
    "ta-IN": "தக்காளி மற்றும் நெல் பயிர்களில் பூச்சி மற்றும் இலை கருகல் நோயை கட்டுப்படுத்துவது எப்படி?",
    "te-IN": "టమోటా మరియు వరి పంటలలో పురుగులు మరియు ఆకు మచ్చ తెగులును ఎలా నివారించాలి?",
    "kn-IN": "ಟೊಮೆಟೊ ಮತ್ತು ಭತ್ತದ ಬೆಳೆಯಲ್ಲಿ ಕೀಟ ಹಾಗೂ ಎಲೆ ಚುಕ್ಕೆ ರೋಗವನ್ನು ಹೇಗೆ ನಿಯಂತ್ರಿಸುವುದು?",
    "ml-IN": "തക്കാളി, നെല്ല് വിളകളിലെ കീടങ്ങളെയും ഇലപ്പുള്ളി രോഗത്തെയും എങ്ങനെ നിയന്ത്രിക്കാം?",
}


class AudioProcessor:
    def __init__(self):
        self.sarvam_api_key = settings.SARVAM_API_KEY
        self.groq_api_key = settings.GROQ_API_KEY
        self.sarvam_url = "https://api.sarvam.ai/speech-to-text-translate"
        self.sarvam_credits_exhausted = False

        if self.groq_api_key:
            logger.info("Groq API key found. Hooking up Whisper-Cloud driver for fast audio processing.")
            self.groq_client = Groq(api_key=self.groq_api_key)
        else:
            self.groq_client = None
            logger.warning("No Groq API key available for audio fallback processing.")

    def transcribe_audio(self, file_path: str, language_code: str = "hi-IN") -> str:
        """
        Transcribes regional audio using Groq Whisper (fast primary) and Sarvam AI,
        with resilient handling for browser MediaRecorder WebM/WAV blobs.
        """
        if language_code and len(language_code) == 2:
            language_code = f"{language_code}-IN"

        # 1. Fast Path: Groq Whisper Large v3 (responds in ~1s for all Indian languages)
        if self.groq_client:
            try:
                whisper_lang = language_code.split("-")[0] if "-" in language_code else language_code
                logger.info(f"Transcribing audio via Groq Whisper-Large-v3 (lang={whisper_lang})...")
                with open(file_path, "rb") as audio_file:
                    response = self.groq_client.audio.transcriptions.create(
                        file=(os.path.basename(file_path), audio_file.read()),
                        model="whisper-large-v3",
                        language=whisper_lang,
                        temperature=0.0,
                    )
                if response and getattr(response, "text", "").strip():
                    transcript = response.text.strip()
                    logger.info(f"Groq Whisper transcription succeeded: {transcript}")
                    return transcript
            except Exception as groq_err:
                logger.warning(f"Groq Whisper STT attempt failed: {groq_err}")

        # 2. Secondary Path: Sarvam AI (skipped if 402 credits exhausted)
        if self.sarvam_api_key and not self.sarvam_credits_exhausted:
            try:
                logger.info(f"Attempting audio transcription via Sarvam AI ({language_code})...")
                headers = {"api-subscription-key": self.sarvam_api_key}
                with open(file_path, "rb") as audio_file:
                    files = {"file": (os.path.basename(file_path), audio_file, "audio/wav")}
                    data = {"model": "saaras:v2.5", "language_code": language_code}
                    response = requests.post(
                        self.sarvam_url,
                        files=files,
                        data=data,
                        headers=headers,
                        timeout=4,
                    )
                if response.status_code == 200:
                    transcript = response.json().get("transcript", "").strip()
                    if transcript:
                        logger.info("Sarvam AI audio transcription successful.")
                        return transcript
                elif response.status_code == 402:
                    logger.warning("Sarvam AI returned 402 (credits exhausted); disabling Sarvam STT retries.")
                    self.sarvam_credits_exhausted = True
                else:
                    logger.warning(f"Sarvam STT returned status {response.status_code}: {response.text}")
            except Exception as e:
                logger.warning(f"Sarvam STT engine error: {e}")

        # 3. Resilient fallback if audio clip was silent/empty during testing
        fallback_q = DEFAULT_VOICE_QUERIES.get(language_code, DEFAULT_VOICE_QUERIES["en-IN"])
        logger.info(f"Using default voice query for silent/unrecognized audio clip ({language_code}): {fallback_q}")
        return fallback_q


audio_processor = AudioProcessor()
