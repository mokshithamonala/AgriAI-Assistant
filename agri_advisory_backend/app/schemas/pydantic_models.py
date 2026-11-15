from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TextQueryRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the session context tracking")
    text: str = Field(..., description="The raw incoming text question from the farmer")
    preferred_language: Optional[str] = Field(
        "auto", 
        description="Supported codes: hi-IN (Hindi), kn-IN (Kannada), te-IN (Telugu), ta-IN (Tamil), ml-IN (Malayalam)"
    )

class APIResponseSchema(BaseModel):
    session_id: str
    detected_language: str
    canonical_query: str
    inferred_intent: str
    extracted_agricultural_entities: Dict[str, Any]
    canonical_response: str
    translated_response: str