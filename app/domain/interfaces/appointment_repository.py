"""Appointment repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.appointment import Appointment
from app.domain.entities.slot import Slot


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
    async def update_appointment(self, appointment: Appointment) -> Appointment:
        ...

    @abstractmethod
    async def get_slot_available(self, slot_id: str) -> Optional[Slot]:
        ...

    @abstractmethod
    async def mark_slot_as_booked(self, slot_id: str) -> None:
        ...