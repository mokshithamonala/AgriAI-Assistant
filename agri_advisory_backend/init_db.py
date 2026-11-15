# init_db.py
from app.db.database import engine, Base
from app.db.models import ConversationState
from app.core.logger import logger

def initialize_tables():
    logger.info("Creating tables in Supabase...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully!")

if __name__ == "__main__":
    initialize_tables()