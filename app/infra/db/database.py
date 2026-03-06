import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.infra.core.logging import get_logger

logger = get_logger("DB")


async def check_db_connection() -> None:
    """Check DB connectivity using the async engine."""
    engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
    finally:
        await engine.dispose()