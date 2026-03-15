"""Appointment DTOs."""

from __future__ import annotations
from app.common import *
from dataclasses import dataclass


@dataclass(frozen=True)
class AppointmentDTO:
    customer_id: str
    branch_id: str
    slot_id: str
    service_type_id: str
    staff_id: str
    attachment_path: Optional[UploadFile] = None



__all__ = [
    "AppointmentDTO",
]
