"""Concrete appointment-repository implementation."""

from __future__ import annotations

from typing import Optional

from app.domain.entities.appointment import Appointment
from app.domain.interfaces.appointment_repository import AppointmentRepository


class AppointmentRepositoryImpl(AppointmentRepository):
    """SQLAlchemy async implementation of AppointmentRepository."""

    async def create_appointment(self, appointment: Appointment) -> Appointment:
        # TODO: implement with async session
        return appointment

    async def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        # TODO: implement
        return None

    async def get_appointments(self) -> list[Appointment]:
        # TODO: implement
        return []
