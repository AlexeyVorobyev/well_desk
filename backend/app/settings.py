from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Well Desk API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 3000

    database_url: str = "sqlite:///./well_desk.db"

    openai_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None

    default_user_id: str = "default-user"
    summary_enabled: bool = True

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance to avoid reparsing env variables."""

    return Settings()
