"""FlowCare application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.config import get_settings
from app.api.v1.routers import api_router
from app.api.middleware import add_exception_handlers

settings = get_settings()


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
    )

    add_exception_handlers(app)

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
