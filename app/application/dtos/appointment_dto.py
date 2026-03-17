"""Appointment DTOs."""

from __future__ import annotations
from app.common import Optional, UploadFile
from dataclasses import dataclass


@dataclass(frozen=True)
class AppointmentDTO:
    customer_id: str
    branch_id: str
    slot_id: str
    service_type_id: Optional[str] = None
    staff_id: Optional[str] = None
    attachment: Optional[UploadFile] = None


__all__ = [
    "AppointmentDTO",
]
