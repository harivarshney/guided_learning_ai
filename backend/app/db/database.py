"""
Database Connection Setup
Connects to Railway PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Test connection before using
    echo=False  # Set to True for debugging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    """Get database session for API routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables on startup
def init_db():
    """Create all tables in database"""
    Base.metadata.create_all(bind=engine)