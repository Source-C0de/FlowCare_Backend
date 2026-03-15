from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # JWT
    JWT_SECRET_KEY: str = "8d7a2e3f4b9c1a6f0d8e5c3b7f2a9d1c4e6b8f0a3c5d7e9f1a2b4c6d8e0f3a5"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    # COOKIE
    COOKIE_DOMAIN: str | None = None          # None = same host
    COOKIE_SECURE: bool = True                # False only for local HTTP dev
    COOKIE_SAMESITE: str = "strict"
    REFRESH_COOKIE_NAME: str = "refresh_token"
    ACCESS_COOKIE_NAME: str = "access_token"


    #RATE LIMIT
    RATE_LIMIT_BOOKINGS_PER_DAY: int = 2

    # ── Argon2id params ──────────────────────────────────────
    ARGON2_TIME_COST: int = 3
    ARGON2_MEMORY_COST: int = 65536           # 64 MB
    ARGON2_PARALLELISM: int = 4


    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    LOG_LEVEL: str = "INFO"
    
    
    DEBUG: bool = True

    # Role wise define Value
    ADMIN: int = 1
    BRANCH_MANAGER: int = 2
    STAFF: int  = 3
    CUSTOMER: int = 4


    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "flowcare"
    MINIO_REGION: str = "us-east-1"
    MINIO_SECURE: bool = False

    CUSTOMER_ID_MAX_SIZE: int = 5 * 1024 * 1024
    ATTACHMENT_MAX_SIZE: int = 5 * 1024 * 1024


    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

# Singleton pattern - called hundred of times , init once
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()