import datetime
from sqlalchemy import Column, String, DateTime, JSON
from app.db.database import Base

class ConversationState(Base):
    __tablename__ = "conversation_states"

    session_id = Column(String, primary_key=True, index=True, nullable=False)
    detected_language = Column(String, default="en", nullable=False)
    preferred_language = Column(String, default="en", nullable=False)
    
    # Stores raw conversation history as a JSON list: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    conversation_history = Column(JSON, default=list, nullable=False)
    
    # Stores dynamic user preferences (e.g., preferred crops, location)
    user_preferences = Column(JSON, default=dict, nullable=False)
    
    # Stores internal context markers (e.g., current topic: 'pest_control')
    context = Column(JSON, default=dict, nullable=False)
    
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)