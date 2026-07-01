import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

# Get the root directory (2 levels up from this file)
ROOT_DIR = Path(__file__).parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    serper_api_key: str = os.getenv("SERPER_API_KEY", "")
    news_api_key: str = os.getenv("NEWS_API_KEY", "")
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/guided_learning"
    )
    
    # URLs
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM Model
    groq_model: str = "llama-3.3-70b-versatile"
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export for easy importing
settings = get_settings()