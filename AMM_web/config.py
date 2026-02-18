"""
Global configuration using pydantic-settings.
All environment variables are automatically loaded.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application configuration."""

    API_BASE_URL: str = "https://127.0.0.1:8000/"
    API_TIMEOUT: int = 10
    SITE_NAME: str = "AMM Web Client"
    SITE_DESCRIPTION: str = "A modular Reflex-based Audiophiles' Music Manager interface."
    SENTRY_DSN: Optional[str] = None

    CONTACT_TO_EMAIL: str = "pegasus.ict@gmail.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AMM_", extra="ignore")


settings = Settings()
