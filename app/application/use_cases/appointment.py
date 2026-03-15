"""Book-appointment use case."""

from __future__ import annotations

from app.domain.exceptions import ValidationException
from app.domain.interfaces.appointment_repository import AppointmentRepository


class BookAppointmentUseCase:
    """Orchestrates appointment booking."""

    def __init__(self, appointment_repo: AppointmentRepository) -> None:
        self._repo = appointment_repo

    async def execute(
        self,
        customer_id: str,
        branch_id: str,
        service_type_id: str,
        slot_id: str,
        staff_id: str,
    ) -> dict:
        # TODO: implement slot availability check via repository
        # TODO: implement daily booking limit check

        # Placeholder — create appointment through repository
        result = await self._repo.create_appointment(
            appointment=None  # type: ignore  # will be a proper entity once slot logic is wired
        )
        return result



__all__ = [
    "BookAppointmentUseCase"
]
