from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
from app.core.logger import logger

Base = declarative_base()

try:
    # pool_pre_ping=True checks the connection viability before executing queries
    # essential for cloud databases like Supabase which can drop idle links
    engine = create_engine(
        settings.DATABASE_URL, 
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"connect_timeout": 5}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine initialized successfully.")
except Exception as e:
    logger.warning(f"PostgreSQL driver/connection unavailable ({str(e)}). Falling back to local SQLite database.")
    engine = create_engine(
        "sqlite:///./sql_app.db",
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()