"""V1 API router — aggregates all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.appointment import router as appointment_router
from app.api.v1.endpoints.branch import router as branch_router
from app.api.v1.endpoints.service_type import router as service_type_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(appointment_router, tags=["Appointment"])
api_router.include_router(branch_router, tags=["Branch"])
api_router.include_router(service_type_router, tags=["Service Type"])
