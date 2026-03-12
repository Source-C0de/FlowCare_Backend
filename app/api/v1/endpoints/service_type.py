"""Service type endpoints."""

from app.common import APIRouter, Depends, status

router = APIRouter(prefix="/service-types", tags=["Service Types"])