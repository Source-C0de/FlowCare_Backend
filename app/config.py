from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: str = "local"
    app_name: str = "FlowCare"
    log_level: str = "INFO"

    # DB (not prefixed, to match common deployment env vars)
    database_url: str = Field(
        default="postgresql+asyncpg://testcare:testcare@localhost:5432/testcare",
        validation_alias="DATABASE_URL",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
