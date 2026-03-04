"""
Simplified Configuration - Internal Use
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Simplified settings for internal use"""
    
    # App
    DEBUG: bool = True
    
    # Database (SQLite for simplicity, can use PostgreSQL in production)
    DATABASE_URL: str = "sqlite+aiosqlite:///./avatarkit.db"
    
    # API Keys - set via environment or accept missing for dev
    FAL_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    
    # Optional: R2 storage (if not set, saves locally)
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "avatarkit"
    
    # Local storage path (fallback when R2 not configured)
    LOCAL_STORAGE_PATH: str = "./storage"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
