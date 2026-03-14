"""Appointment API schemas."""

from __future__ import annotations
from app.common import Optional, BaseModel


class AppointmentDetails(BaseModel):
    branch_id: str
    service_type_id: str
    staff_id: str
    start_time: str
    end_time: str
    capacity: int
    is_active: bool


class CreateAppointmentRequest(BaseModel):
    branch_id: str
    slot_id: str
    service_type_id: str
    staff_id: str
    start_time: str
    end_time: str


class CreateAppointmentResponse(BaseModel):
    status: str
    message: str
    data: AppointmentDetails


class CancelAppointmentRequest(BaseModel):
    appointment_id: str


class CancelAppointmentResponse(BaseModel):
    status: str
    message: str
    data: AppointmentDetails


class UpdateAppointmentRequest(BaseModel):
    appointment_id: str


__all__ = [
    "AppointmentDetails",
    "CreateAppointmentRequest",
    "CreateAppointmentResponse",
    "CancelAppointmentRequest",
    "CancelAppointmentResponse",
    "UpdateAppointmentRequest",
]
