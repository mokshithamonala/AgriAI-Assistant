import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agri-Based Agricultural Advisory System"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    
    # Third-Party APIs
    SARVAM_API_KEY: str = Field(..., validation_alias="SARVAM_API_KEY")
    HUGGINGFACE_API_KEY: str = Field(..., validation_alias="HUGGINGFACE_API_KEY")
    
    # Groq Cloud Integration (Your New Live Free-Tier Driver)
    GROQ_API_KEY: Optional[str] = Field(None, validation_alias="GROQ_API_KEY")
    
    # OpenAI (Now marked Optional so the server doesn't crash without a key)
    OPENAI_API_KEY: Optional[str] = Field(None, validation_alias="OPENAI_API_KEY")

    # Read from .env file
    model_config = SettingsConfigDict(env_file=str(ENV_FILE_PATH), env_file_encoding="utf-8", extra="ignore")

settings = Settings()