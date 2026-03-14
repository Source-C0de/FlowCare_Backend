"""Appointment DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppointmentDTO:
    branch_id: str
    service_type_id: str
    staff_id: str
    slot_id: str
    start_time: str
    end_time: str



__all__ = [
    "AppointmentDTO",
]
