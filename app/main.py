
from fastapi import FastAPI

from app.config import get_settings

from app.core.logging import configure_logging
from app.api.v1.routers import api_router

def project_init() -> FastAPI:
    
    
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI()    
    
    app.include_router(api_router, prefix="/api/v1")
    return app

app = project_init()