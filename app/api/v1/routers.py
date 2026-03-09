from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.controllers.auth import router as auth_router
from app.api.v1.controllers.appointment import router as appointment_router


api_router = APIRouter()


#All router path
api_router.include_router(health_router, tags = ["health"])
api_router.include_router(auth_router, tags = ["Authentication"])
api_router.include_router(appointment_router, tags = ["Appointment"])
