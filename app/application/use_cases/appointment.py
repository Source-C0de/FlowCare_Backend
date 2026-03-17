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
from app.application.dtos.common_dto import PaginationDTO


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
                branch_id = dto.branch_id,
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


    async def get_all_appointments(self, branch_id: str | None = None, staff_id: str | None = None, pagination: PaginationDTO | None = None) -> list[Appointment]:
        return await self._repo.get_all_appointments(branch_id, staff_id, pagination)       


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

        result = await self._repo.cancel_appointment(appointment_id)

        await self._audit_repo.write_audit_log(
            AuditLog(
                action="appointment_cancelled",
                actor_id=UUID(user_id) if isinstance(user_id, str) else user_id,
                actor_role="customer",
                entity_id=appointment.id,
                entity_type="appointment",
                branch_id=str(appointment.branch_id) if appointment.branch_id else None,
                metadata={
                    "slot_id": str(appointment.slot_id) if appointment.slot_id else None,
                    "staff_id": str(appointment.staff_id) if appointment.staff_id else None,
                    "status": appointment.status.value,
                },
            )
        )

        return result

    async def reschedule_appointment(self,appointment_id: str, user_id: str, slot_id: str) -> Appointment:
        appointment = await self._repo.get_appointment(appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")
        
        # Security check: only the owner can update
        if str(appointment.customer_id) != user_id:
            raise ForbiddenException("You don't have permission to update this appointment")
            
        if appointment.status != AppointmentStatus.BOOKED:
            raise ValidationException("Only Booked appointment can be updated")
        
        # appointment.status = AppointmentStatus.CANCELLED
        result = await self._repo.update_appointment(appointment_id, slot_id)

        await self._audit_repo.write_audit_log(
            AuditLog(
                action="appointment_rescheduled",
                actor_id=UUID(user_id) if isinstance(user_id, str) else user_id,
                actor_role="customer",
                entity_id=appointment.id,
                entity_type="appointment",
                branch_id=str(appointment.branch_id) if appointment.branch_id else None,
                metadata={
                    "slot_id": str(appointment.slot_id) if appointment.slot_id else None,
                    "staff_id": str(appointment.staff_id) if appointment.staff_id else None,
                    "status": appointment.status.value,
                },
            )
        )
        return result
        
    async def get_appointment_details(self, appointment_id: str, current_user: tuple[User, str]) -> Appointment:

        user, role = current_user
        appointment = await self._repo.get_appointment(appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")
        
        # Security check
        if role == "CUSTOMER" and str(appointment.customer_id) != str(user.id):
            raise ForbiddenException("Access denied")
        
        if role == "BRANCH_MANAGER" and str(appointment.branch_id) != str(user.branch_id):
            raise ForbiddenException("Access denied!\nNot your branch")
        
        if role == "STAFF" and str(appointment.staff_id) != str(user.id):
            raise ForbiddenException("Access denied!\nNot assigned to you")
        
        return appointment

    async def update_appointment_status(self, appointment_id: str, status: AppointmentStatus, actor_id: str, actor_role: str, branch_id: str | None = None) -> Appointment:
        appointment = await self._repo.get_appointment(appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")
        if branch_id and str(appointment.branch_id) != branch_id:
            raise ForbiddenException("Access denied!\nNot your branch")

        result = await self._repo.update_appointment_status(appointment_id, status)
        await self._audit_repo.write_audit_log(
            AuditLog(
                action="appointment_status_updated",
                actor_id=UUID(actor_id) if isinstance(actor_id, str) else actor_id,
                actor_role=actor_role,
                entity_id=appointment.id,
                entity_type="appointment",
                branch_id=str(appointment.branch_id) if appointment.branch_id else None,
                metadata={
                    "status": result.status.value,
                },
            )
        )
        return result

    async def get_queue_position(self, branch_id: str, user_id: str) -> dict:

        result = await self._repo.get_queue_position(branch_id)
        return result
        


__all__ = [
    "AppointmentUseCase"
]
