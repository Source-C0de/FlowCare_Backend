from __future__ import annotations

from app.common import BaseModel

class ServiceType(BaseModel):
    id: str
    branch_id: str
    name: str
    description: str
    duration: int
    is_active: bool
    created_at: str
    updated_at: str


class CreateServiceTypeRequest(BaseModel):
    name: str
    branch_id: str 
    description: str
    duration_minutes: int



from typing import Optional

class UpdateServiceTypeRequest(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    branch_id: Optional[str] = None
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
