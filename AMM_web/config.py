"""
Global configuration using pydantic-settings.
All environment variables are automatically loaded.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application configuration."""

    API_BASE_URL: str = "https://api.amm.local"
    API_TIMEOUT: int = 10
    SITE_NAME: str = "AMM Web Client"
    SITE_DESCRIPTION: str = "A modular Reflex-based Automated Market Maker interface."
    SENTRY_DSN: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AMM_")


settings = Settings()
