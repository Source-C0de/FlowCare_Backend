from __future__ import annotations

from pydantic import ConfigDict
from app.common import BaseModel, Optional, datetime

class ServiceType(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    branch_id: str
    name: str
    description: str
    duration_minutes: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ServiceTypeRequest(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int


class UpdateServiceTypeRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class DeleteServiceTypeRequest(BaseModel):
    id: str


class GetServiceTypeRequest(BaseModel):
    id: str


class GetServiceTypesRequest(BaseModel):
    pass


class CreateServiceTypeResponse(BaseModel):
    status: str
    message: str
    data: ServiceType


class UpdateServiceTypeResponse(BaseModel):
    status: str
    message: str
    data: ServiceType


class DeleteServiceTypeResponse(BaseModel):
    status: str
    message: str
    data: ServiceType


class GetServiceTypeResponse(BaseModel):
    status: str
    message: str
    data: ServiceType


class GetServiceTypesResponse(BaseModel):
    status: str
    message: str
    data: list[ServiceType]


class ServiceTypeResponse(BaseModel):
    status: str
    message: str
    data: ServiceType


__all__ = [
    "ServiceType",
    "ServiceTypeRequest",
    "UpdateServiceTypeRequest",
    "DeleteServiceTypeRequest",
    "GetServiceTypeRequest",
    "GetServiceTypesRequest",
    "CreateServiceTypeResponse",
    "UpdateServiceTypeResponse",
    "DeleteServiceTypeResponse",
    "GetServiceTypeResponse",
    "GetServiceTypesResponse",
    "ServiceTypeResponse",
]
