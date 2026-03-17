"""Appointment repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.appointment import Appointment
from app.domain.entities.slot import Slot
from app.api.v1.schemas.common import PaginationRequest


class AppointmentRepository(ABC):
    """Defines the contract for appointment persistence."""

    @abstractmethod
    async def create_appointment(self, appointment: Appointment) -> Appointment:
        ...

    @abstractmethod
    async def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        ...

    @abstractmethod
    async def get_appointments_by_user(self, user_id: str) -> list[Appointment]:
        ...
    
    @abstractmethod
    async def get_all_appointments(self, branch_id: str | None = None, staff_id: str | None = None, pagination: PaginationRequest | None = None) -> list[Appointment]:
        ...
    
    @abstractmethod
    async def update_appointment(self, appointment_id: str, slot_id: str) -> Appointment:
        ...

    @abstractmethod
    async def get_slot_available(self, slot_id: str) -> Optional[Slot]:
        ...

    @abstractmethod
    async def mark_slot_as_booked(self, slot_id: str) -> None:
        ...

    @abstractmethod
    async def cancel_appointment(self, appointment_id: str) -> Appointment:
        ...


    @abstractmethod
    async def get_queue_position(self, branch_id: str) -> dict:
        ...

    @abstractmethod
    async def update_appointment_status(self, appointment_id: str, status: AppointmentStatus) -> Appointment:
        ...