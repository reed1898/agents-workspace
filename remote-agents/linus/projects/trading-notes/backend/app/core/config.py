from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Project
    PROJECT_NAME: str = "Trading Notes API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Security
    SECRET_KEY: str
    ENCRYPTION_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/auth/google/callback"
    GOOGLE_GMAIL_CLIENT_ID: str = ""
    GOOGLE_GMAIL_CLIENT_SECRET: str = ""
    GOOGLE_GMAIL_REDIRECT_URI: str = "http://localhost:8000/api/v1/import/gmail/oauth/callback"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
