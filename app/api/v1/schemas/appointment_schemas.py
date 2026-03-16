"""Appointment API schemas."""

from __future__ import annotations
from app.common import *
from fastapi import Form, File


class AppointmentDetails(BaseModel):
    id: str
    appointment_no: str
    branch_id: str
    service_type_id: str
    staff_id: str
    status: str
    slot_id: str
    attachment_path: Optional[str] = None

class CreateAppointmentRequest(BaseModel):
    branch_id: str = Form(...)
    slot_id: str = Form(...)
    service_type_id: Optional[str] = Form(None)
    staff_id: Optional[str] = Form(None)
    attachment: Optional[UploadFile] = File(None)


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
