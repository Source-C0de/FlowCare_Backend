"""FlowCare application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.config import get_settings
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request


from app.api.middleware import add_exception_handlers

from contextlib import asynccontextmanager
from scripts.seed_db import seed_from_json
from app.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed database
    logger.info("Initializing database seeding...")
    try:
        await seed_from_json()
        logger.info("Database seeding completed.")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
    yield
    # Shutdown logic (none needed)

def create_app() -> FastAPI:
    """Application factory — creates and configures the FastAPI instance."""
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    app = FastAPI(
        title="Queue & Appointment API",
        description="API for managing appointments and queue system",
        version="1.0.0",
        docs_url="/flowcare/docs",
        redoc_url="/flowcare/redoc",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": str(exc) if settings.DEBUG else "Internal server error"})

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
