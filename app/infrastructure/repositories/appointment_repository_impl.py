"""Concrete appointment-repository implementation."""

from __future__ import annotations

from app.common import *
from app.domain.entities.appointment import *
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.infrastructure.models.appointment_model import Appointment as AppointmentModel
from app.infrastructure.models.slot_model import Slot as SlotModel
from app.infrastructure.models.audit_log_model import AuditLog as AuditLogModel
from app.domain.entities.slot import Slot
from app.api.v1.schemas.common import PaginationRequest

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
            service_type_id=str(model.service_type_id) if model.service_type_id else None,
            slot_id=str(model.slot_id) if model.slot_id else None,
            staff_id=str(model.staff_id) if model.staff_id else None,
            status=model.status,
            attachment_path=model.attachment_path if model.attachment_path else None
        )

    async def create_appointment(
        self, appointment: Appointment
    ) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                # 1. Fetch and Lock the Slot
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

                # 2. Create Appointment Model
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
                
                # 3. Mark Slot as Booked
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
            if not model:
                raise DomainException("Appointment not found")
            return self._to_entity(model)     

    async def get_appointments_by_user(self, user_id: str) -> list[Appointment]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AppointmentModel).where(AppointmentModel.customer_id == user_id)
            )
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def get_all_appointments(self, branch_id: str | None = None, staff_id: str | None = None, pagination: PaginationRequest | None = None) -> list[Appointment]:
        async with AsyncSessionLocal() as session:
            query = select(AppointmentModel)
            if branch_id:
                query = query.where(AppointmentModel.branch_id == branch_id)
            if staff_id:
                query = query.where(AppointmentModel.staff_id == int(staff_id))
            
            if pagination:
                query = query.offset(pagination.offset).limit(pagination.limit)
                
            result = await session.execute(query)
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]

    async def update_appointment(self, appointment_id: str, slot_id: str) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(AppointmentModel).where(AppointmentModel.appoinment_no == appointment_id)
                )
                appt_model = result.scalar_one_or_none()
                if not appt_model:
                    raise DomainException("Appointment not found")

                current_slot_id = str(appt_model.slot_id) if appt_model.slot_id else None
                new_slot_id = str(slot_id) if slot_id else None

                if current_slot_id != new_slot_id:
                    if appt_model.slot_id:
                        old_slot_res = await session.execute(
                            select(SlotModel).where(SlotModel.id == appt_model.slot_id)
                        )
                        old_slot = old_slot_res.scalar_one_or_none()
                        if old_slot:
                            old_slot.is_booked = False
                    if new_slot_id:
                        new_slot_res = await session.execute(
                            select(SlotModel).where(SlotModel.id == new_slot_id)
                        )
                        new_slot = new_slot_res.scalar_one_or_none()
                        if new_slot:
                            new_slot.is_booked = True

                        appt_model.slot_id = new_slot_id
                        appt_model.branch_id = new_slot.branch_id
                        appt_model.service_type_id = new_slot.service_type_id
                        appt_model.staff_id = new_slot.staff_id
                        appt_model.status = AppointmentStatus.BOOKED 

                await session.commit()
                return self._to_entity(appt_model)
            except Exception as e:
                await session.rollback()
                raise DomainException(str(e))


    async def cancel_appointment(self, appointment_id: str) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(AppointmentModel).where(AppointmentModel.appoinment_no == appointment_id)
                )
                appt_model = result.scalar_one_or_none()
                
                if not appt_model:    
                    raise DomainException("Appointment not found")

                # 2. Fetch Slot Model using THIS session
                if appt_model.slot_id:
                    slot_result = await session.execute(
                        select(SlotModel).where(SlotModel.id == appt_model.slot_id)
                    )
                    slot_model = slot_result.scalar_one_or_none()
                    
                    if slot_model:
                        # Modify the tracked model directly
                        slot_model.is_booked = False
                appt_model.status = AppointmentStatus.CANCELLED
                await session.commit()
                return self._to_entity(appt_model)
            except Exception as e:
                await session.rollback()
                raise DomainException(str(e))

    async def update_appointment_status(self, appointment_id: str, status: AppointmentStatus) -> Appointment:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(AppointmentModel).where(AppointmentModel.appoinment_no == appointment_id)
                )
                appt_model = result.scalar_one_or_none()
                if not appt_model:
                    raise DomainException("Appointment not found")
                appt_model.status = status
                await session.commit()
                return self._to_entity(appt_model)
            except Exception as e:
                await session.rollback()
                raise DomainException(str(e))   

    async def get_slot_available(self, slot_id: str) -> Optional[Slot]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
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

    async def get_queue_position(self, branch_id: str) -> dict:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(func.count()).select_from(AppointmentModel).where(
                    AppointmentModel.branch_id == branch_id,
                    AppointmentModel.status == AppointmentStatus.BOOKED
                )
            )
            total_waiting = result.scalars().first()
            return {
                "branch_id": branch_id,
                "total_waiting": total_waiting
            }

    async def mark_slot_as_booked(self, slot_id: str) -> None:
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(SlotModel)
                .where(SlotModel.id == slot_id)
                .values(is_booked=True)
            )
            await session.commit()