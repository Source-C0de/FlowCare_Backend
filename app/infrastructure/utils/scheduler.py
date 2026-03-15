from __future__ import annotations

from app.common import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.system_config import SystemConfig
from app.services.slot_service import cleanup_expired_slots
import logging 
logger = get_logger(__name__)
scheduler = AsyncIOScheduler()

async def _run_cleanup():
    logger.info("⏰ Scheduler: running slot cleanup job...")
    async with AsyncSessionLocal() as db:
        try:
            config = await db.get(SystemConfig, "retention_period_days")
            retention_days = int(config.value) if config else 30
            count = await cleanup_expired_slots(db, retention_days, actor_id=0, actor_role="system")
            await db.commit()
            logger.info(f"⏰ Scheduler: hard-deleted {count} expired slot(s)")
        except Exception as e:
            await db.rollback()
            logger.error(f"⏰ Scheduler cleanup failed: {e}")


def start_scheduler():
    scheduler.add_job(_run_cleanup, CronTrigger(hour=0, minute=0), id="cleanup_slots", replace_existing=True)
    scheduler.start()
    logger.info("⏰ Background scheduler started (daily cleanup at midnight)")


def stop_scheduler():
    scheduler.shutdown(wait=False)

