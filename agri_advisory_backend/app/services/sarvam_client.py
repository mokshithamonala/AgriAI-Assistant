import requests
import json
from typing import Optional
from app.core.config import settings
from app.core.logger import logger

class SarvamAIClient:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.headers = {
            "api-subscription-key": self.api_key,  # <--- Change this back to what Sarvam requires!
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.sarvam.ai"

    def _format_language_code(self, lang_code: str) -> str:
        """ Ensures 2-character codes (e.g., 'ml', 'hi') are normalized to 'ml-IN', 'hi-IN' """
        if lang_code and len(lang_code) == 2:
            return f"{lang_code}-IN"
        return lang_code

    def translate(self, text: str, source_lang: str, target_lang: str = "en-IN") -> Optional[str]:
        """
        Translates text to the canonical language (English) or back to regional language.
        """
        endpoint = f"{self.base_url}/translate"
        
        # Enforce strict BCP-47 validation parameters
        src = self._format_language_code(source_lang)
        tgt = self._format_language_code(target_lang)

        payload = {
            "input": text,  # Sarvam expects a clean flat string string input 
            "source_language_code": src,
            "target_language_code": tgt,
            "speaker_gender": "Male",
            "mode": "formal",
            "model": "mayura:v1"  # Correct production-tier structural translation model ID
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # The API returns an object structured as {"translated_text": "string"}
            translated_text = response.json().get("translated_text", "")
            logger.info(f"Successfully translated '{src}' to '{tgt}' via Sarvam.")
            return translated_text
        except Exception as e:
            logger.error(f"Sarvam Translation API error: {str(e)}")
            return None

    def speech_to_text(self, audio_file_path: str, language_code: str) -> Optional[str]:
        """
        Converts Hindi/Kannada speech to text.
        """
        endpoint = f"{self.base_url}/speech-to-text-translate"
        lang = self._format_language_code(language_code)
        
        try:
            # For multi-part file payloads, we do not provide a Content-Type string header
            headers = {"api-subscription-key": self.api_key}
            with open(audio_file_path, 'rb') as f:
                files = {'file': (audio_file_path, f, 'audio/wav')}
                data = {'model': 'saaras:v1', 'language_code': lang}
                
                response = requests.post(endpoint, headers=headers, files=files, data=data)
                response.raise_for_status()
                
            transcript = response.json().get("transcript", "")
            logger.info(f"Sarvam STT successful for {lang}.")
            return transcript
        except Exception as e:
            logger.error(f"Sarvam STT API error: {str(e)}")
            return None

    def text_to_speech(self, text: str, language_code: str) -> Optional[bytes]:
        """
        Converts text back into regional language speech.
        """
        endpoint = f"{self.base_url}/text-to-speech"
        lang = self._format_language_code(language_code)

        payload = {
            "inputs": [text],
            "target_language_code": lang,
            "speaker": "meera", 
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            audio_content = response.json()["audios"][0] 
            logger.info(f"Sarvam TTS generated for {lang}.")
            return audio_content
        except Exception as e:
            logger.error(f"Sarvam TTS API error: {str(e)}")
            return None

# Singleton instance for the app to use
sarvam_client = SarvamAIClient()