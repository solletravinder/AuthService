from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
import time
import logging
from config import settings

GLOBAL_PATH = settings.GLOBAL_PATH

logger = logging.getLogger(__name__)

# Configure database with connection pooling and advanced options
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enables connection pre-ping
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_timeout=30,     # Wait up to 30 seconds for a connection
    pool_size=5,         # Maintain up to 5 connections
    max_overflow=10,     # Allow up to 10 more connections in high load
    echo=False,          # Set to True to log all SQL queries (very verbose)
    connect_args={
        "connect_timeout": 10,  # Timeout of 10 seconds when connecting
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Set up connection retry logic
MAX_RETRIES = 3
RETRY_BACKOFF = 0.5  # Start with 0.5 second delay

# Dependency to get DB session with retry logic
def get_db() -> Generator:
    db = None
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            db = SessionLocal()
            # Test connection is working
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            break
        except Exception as e:
            if db:
                db.close()
            
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Failed to connect to database after {MAX_RETRIES} attempts")
                raise
                
            # Exponential backoff
            sleep_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Database connection failed, retrying in {sleep_time}s... ({retries}/{MAX_RETRIES})")
            time.sleep(sleep_time)
    
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if db:
            db.close()

# Create all tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
