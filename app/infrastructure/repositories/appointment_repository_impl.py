"""Concrete appointment-repository implementation."""

from __future__ import annotations

from app.common import *
from app.domain.entities.appointment import Appointment, AppointmentStatus
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.infrastructure.models.appointment_model import Appointment as AppointmentModel
from app.infrastructure.models.slot_model import Slot as SlotModel
from app.infrastructure.models.audit_log_model import AuditLog as AuditLogModel
from app.domain.entities.slot import Slot

class AppointmentRepositoryImpl(AppointmentRepository):
    """SQLAlchemy async implementation of AppointmentRepository."""
    def __init__(self):
        pass
    def _to_entity(self, model: AppointmentModel) -> Appointment:
        return Appointment(
            id=model.id,
            appoinment_no=model.appoinment_no,
            customer_id=model.customer_id,
            branch_id=model.branch_id,
            service_type_id=model.service_type_id,
            slot_id=model.slot_id,
            staff_id=model.staff_id,
            status=model.status,
            attachment_path=model.attachment_path,
        )

    async def create_appointment(
        self, appointment: Appointment
    ) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                # Use internal model retrieval for transaction safety
                slot_result = await session.execute(
                    select(SlotModel).where(
                        SlotModel.id == appointment.slot_id,
                        SlotModel.is_active == True,
                        SlotModel.is_booked == False
                    ).with_for_update(skip_locked=True)
                )
                slot = slot_result.scalar_one_or_none()
                if not slot:
                    raise DomainException("Slot not found or already booked")

                model = AppointmentModel(
                    id=appointment.id,
                    appoinment_no=appointment.appoinment_no,
                    customer_id=appointment.customer_id,
                    branch_id=appointment.branch_id,
                    service_type_id=appointment.service_type_id,
                    slot_id=appointment.slot_id,
                    staff_id=appointment.staff_id,
                    status=appointment.status,
                    attachment_path=appointment.attachment_path,
                )
                session.add(model)
                slot.is_booked = True
                
                await session.flush()
                await session.commit()
                return self._to_entity(model)
            except DomainException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                raise DomainException(str(e))

    async def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AppointmentModel).where(AppointmentModel.appoinment_no == appointment_id)
            )
            model = result.scalar_one_or_none()
            return self._to_entity(model) if model else None

    async def get_appointments_by_user(self, user_id: str) -> list[Appointment]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AppointmentModel).where(AppointmentModel.customer_id == user_id)
            )
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def update_appointment(self, appointment: Appointment) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                appt = await self.get_appointment(appointment.id)
                if not appt:
                    raise DomainException("Appointment not found")
                
                if appt.slot_id:
                    slot = await self.get_slot_available(appt.slot_id)
                    if slot:
                        slot.is_booked = False
                
                appt.status = appointment.status
                await session.flush()
                await session.commit()
                await session.refresh(appt)
                return self._to_entity(appt)
            except Exception as e:
                await session.rollback()
                raise DomainException(str(e))

    async def get_slot_available(self, slot_id: str, session: AsyncSession = None) -> Optional[Slot | SlotModel]:
        """
        Retrieves an available slot. 
        If a session is provided, returns SlotModel (for internal atomic updates).
        Otherwise returns Slot entity (for standard interface use).
        """
        if session:
            result = await session.execute(
                select(SlotModel).where(
                    SlotModel.id == slot_id,
                    SlotModel.is_active == True,
                    SlotModel.is_booked == False
                ).with_for_update(skip_locked=True)
            )
            return result.scalar_one_or_none()
        else:
            async with AsyncSessionLocal() as new_session:
                result = await new_session.execute(
                    select(SlotModel).where(
                        SlotModel.id == slot_id,
                        SlotModel.is_active == True,
                        SlotModel.is_booked == False
                    )
                )
                model = result.scalar_one_or_none()
                if not model:
                    return None
                return Slot(
                    id=model.id,
                    branch_id=model.branch_id,
                    service_type_id=model.service_type_id,
                    is_active=model.is_active,
                    staff_id=str(model.staff_id) if model.staff_id else None,
                    start_time=model.start_time,
                    end_time=model.end_time,
                    is_booked=model.is_booked,
                    capacity=model.capacity
                )

    async def mark_slot_as_booked(self, slot_id: str) -> None:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(SlotModel)
                .where(SlotModel.id == slot_id)
                .values(is_booked=True)
            )
            await session.commit()