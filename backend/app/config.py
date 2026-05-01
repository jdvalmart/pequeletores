"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-specific configuration."""

    model_config = ConfigDict(
        extra="ignore"  # Allow extra fields from .env
    )

    # App settings
    app_name: str = "PequeLectores API"
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://user:pass@localhost:5432/pequelectores"
    )

    # Server - allow both formats
    backend_host: str = Field(default="0.0.0.0")
    backend_port: int = Field(default=8000)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # CORS - stored as comma-separated string, converted to list
    cors_origins_str: str = Field(
        default="http://localhost:5173,http://localhost:3000,https://*.netlify.app,https://*.railway.app"
    )
    
    # Auth settings
    secret_key: str = Field(default="dev-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 24 * 60  # 24 hours

    # Logging
    log_level: str = "INFO"

    @field_validator('cors_origins_str', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        """Parse CORS origins from comma-separated string."""
        if isinstance(v, str):
            return v
        return v
    
    @property
    def cors_origins(self) -> list[str]:
        """Get CORS origins as list."""
        return [origin.strip() for origin in self.cors_origins_str.split(',') if origin.strip()]

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()