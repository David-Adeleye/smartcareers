"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the SmartCareers API."""

    app_name: str = "SmartCareers API"
    environment: str = "development"
    api_version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SMARTCAREERS_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings object for the application."""

    return Settings()
