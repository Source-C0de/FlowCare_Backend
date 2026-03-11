"""Appointment repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.appointment import Appointment


class AppointmentRepository(ABC):
    """Defines the contract for appointment persistence."""

    @abstractmethod
    async def create_appointment(self, appointment: Appointment) -> Appointment:
        ...

    @abstractmethod
    async def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        ...

    @abstractmethod
    async def get_appointments(self) -> list[Appointment]:
        ...
