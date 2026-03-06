
import asyncio
from tabnanny import check

from fastapi import FastAPI

from app.config import get_settings

from app.infra.core.logging import get_logger
from app.infra.db.database import check_db_connection
from app.api.v1.routers import api_router

from app.api.middleware import add_exception_handlers


def project_init() -> FastAPI:

    settings = get_settings()
    get_logger(settings.LOG_LEVEL)
    # run async DB connectivity check before app start
    # asyncio.run(check_db_connection())

    app = FastAPI(
        title="Queue & Appointment API",
        description="Api for mananging appoinments and queue system",
        version="1.0.0",
        docs_url="/flowcare/docs",
        redoc_url="/flowcare/redoc",
    )

    add_exception_handlers(app)

    # Routers calling endpoint
    app.include_router(api_router, prefix="/api/v1")

    return app


app = project_init()
