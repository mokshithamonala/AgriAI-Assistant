from sqlalchemy.orm import Session
from app.db.models import ConversationState
from app.core.logger import logger
from typing import Dict, Any, Optional
import datetime

class StateManager:
    @staticmethod
    def get_or_create_session(db: Session, session_id: str, preferred_lang: str = "en-IN") -> ConversationState:
        """
        Retrieves an active session state by its session_id. 
        If it doesn't exist, a brand new record is initialized in Supabase.
        """
        try:
            state = db.query(ConversationState).filter(ConversationState.session_id == session_id).first()
            
            if not state:
                logger.info(f"Session {session_id} not found. Creating a new entry in Supabase.")
                state = ConversationState(
                    session_id=session_id,
                    detected_language=preferred_lang,
                    preferred_language=preferred_lang,
                    conversation_history=[],
                    user_preferences={},
                    context={}
                )
                db.add(state)
                db.commit()
                db.refresh(state)
            return state
        except Exception as e:
            db.rollback()
            logger.error(f"Error in get_or_create_session for session {session_id}: {str(e)}")
            raise e

    @staticmethod
    def add_message_to_history(db: Session, session_id: str, role: str, content: str) -> Optional[ConversationState]:
        """
        Appends a conversational turn (user query or assistant response) to the state history JSON array.
        """
        try:
            state = StateManager.get_or_create_session(db, session_id)
            
            # SQLAlchemy mutable tracking safety: construct a fresh list instance to ensure changes trigger updates
            updated_history = list(state.conversation_history)
            updated_history.append({
                "role": role,
                "content": content,
                "timestamp": datetime.datetime.utcnow().isoformat()
            })
            
            state.conversation_history = updated_history
            db.commit()
            db.refresh(state)
            return state
        except Exception as e:
            db.rollback()
            logger.error(f"Error appending message to history for session {session_id}: {str(e)}")
            return None

    @staticmethod
    def update_context_and_preferences(
        db: Session, 
        session_id: str, 
        new_context: Dict[str, Any], 
        new_preferences: Dict[str, Any],
        detected_lang: Optional[str] = None
    ) -> Optional[ConversationState]:
        """
        Merges newly extracted NER data, intents, or language preferences into the persistent state session.
        """
        try:
            state = StateManager.get_or_create_session(db, session_id)
            
            # Deep merge dictionary updates safely
            merged_context = dict(state.context)
            merged_context.update(new_context)
            state.context = merged_context
            
            merged_preferences = dict(state.user_preferences)
            merged_preferences.update(new_preferences)
            state.user_preferences = merged_preferences
            
            if detected_lang:
                state.detected_language = detected_lang
                state.preferred_language = detected_lang
                
            db.commit()
            db.refresh(state)
            logger.info(f"Successfully updated metadata parameters for session {session_id}.")
            return state
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating state metadata fields for session {session_id}: {str(e)}")
            return None