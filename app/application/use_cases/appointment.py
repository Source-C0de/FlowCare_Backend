"""Appointment use case."""

from __future__ import annotations

from uuid import uuid4, UUID
from app.common import Optional, UploadFile
from app.domain.entities.appointment import Appointment, AppointmentStatus
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.domain.interfaces.file_repository import FileRepository
from app.application.dtos.appointment_dto import AppointmentDTO
from app.domain.exceptions import ValidationException, ForbiddenException, NotFoundException
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.domain.entities.audit_logs import AuditLog


class AppointmentUseCase:
    """Orchestrates appointment operations."""

    def __init__(
        self, 
        appointment_repo: AppointmentRepository,
        file_repo: FileRepository,
        audit_repo: AuditLogsRepository
    ) -> None:
        self._repo = appointment_repo
        self._file_repo = file_repo
        self._audit_repo = audit_repo

    async def create_appointment(
        self, dto: AppointmentDTO
    ) -> Appointment:
        # TODO: Implement additional validation (slot availability, etc.)
        attachment_path = None
        if dto.attachment:
            attachment_path = await self._file_repo.upload_file(
                file=dto.attachment, 
                folder="appointments"
            )

        # Generate a simple appointment number (e.g., APPT-UUID-Prefix)
        appt_no = f"APPT-{str(uuid4())[:8].upper()}"

        appointment = Appointment(
            id=uuid4(),
            appoinment_no=appt_no,
            customer_id=dto.customer_id,
            branch_id=dto.branch_id,
            service_type_id=dto.service_type_id,
            slot_id=dto.slot_id,
            staff_id=dto.staff_id,
            status=AppointmentStatus.BOOKED,
            attachment_path=attachment_path
        )
        result = await self._repo.create_appointment(appointment)

        await self._audit_repo.write_audit_log(
            AuditLog(
                action="appointment_created",
                actor_id=UUID(dto.customer_id) if isinstance(dto.customer_id, str) else dto.customer_id,
                actor_role="customer",
                entity_id=appointment.id,
                entity_type="appointment",
                metadata={
                    "slot_id": dto.slot_id,
                    "staff_id": dto.staff_id,
                    "status": appointment.status.value,
                },
            )
        )
        return result


    async def get_user_appointments(
        self, user_id: str
    ) -> list[Appointment]:
        return await self._repo.get_appointments_by_user(user_id)


    async def cancel_appointment(
        self, appointment_id: str, user_id: str
    ) -> Appointment:

        appointment = await self._repo.get_appointment(appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")
        
        # Security check: only the owner can cancel
        if str(appointment.customer_id) != user_id:
            raise ForbiddenException("You don't have permission to cancel this appointment")
            
        if appointment.status == AppointmentStatus.CANCELLED:
            raise ValidationException("Appointment is already cancelled")

        appointment.status = AppointmentStatus.CANCELLED
        return await self._repo.update_appointment(appointment)

    async def get_appointment_details(self, appointment_id: str, user_id: str) -> Appointment:
        appointment = await self._repo.get_appointment(appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")
            
        # Security check
        if str(appointment.customer_id) != user_id:
            raise ForbiddenException("Access denied")
            
        return appointment


__all__ = [
    "AppointmentUseCase"
]
