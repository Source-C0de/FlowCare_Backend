"""Database health-check utility."""

from __future__ import annotations

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

logger = logging.getLogger("db.connection")


async def check_db_connection() -> None:
    """Quick async connectivity check."""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
    except Exception as exc:
        logger.error("❌ Database connection failed: %s", exc)
    finally:
        await engine.dispose()
