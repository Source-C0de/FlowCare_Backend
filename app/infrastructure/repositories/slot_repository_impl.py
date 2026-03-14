from __future__ import annotations

from app.infrastructure.database.session import AsyncSessionLocal
from app.domain.interfaces.slot_repository import SlotRepository
from app.domain.entities.slot import Slot
from app.application.dtos.slot_dto import SlotDTO
from app.domain.exceptions import DomainException
from sqlalchemy import insert,select,func,delete
from app.infrastructure.models.slot_model import Slot as SlotModel
from app.api.v1.schemas.slot_schemas import GetSlotsRequest

class SlotRepositoryImpl(SlotRepository):
    async def get_slots(self, dto: GetSlotsRequest) -> list[Slot]:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(SlotModel)
                    .where(SlotModel.branch_id == dto.branch_id)
                    .where(SlotModel.service_type_id == dto.service_type_id)
                    .where(SlotModel.is_active == True)
                )
                models = result.scalars().all()
                return [
                    Slot(
                        id=model.id,
                        branch_id=model.branch_id,
                        service_type_id=model.service_type_id,
                        staff_id=model.staff_id,
                        start_time=model.start_time,
                        end_time=model.end_time,
                        is_booked=model.is_booked,
                        capacity=model.capacity,
                        is_active=model.is_active
                    ) for model in models
                ]
        except Exception as e:
            raise DomainException(str(e))
    
    async def get_slot_by_id(self, slot_id: UUID) -> Slot:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(SlotModel)
                    .where(SlotModel.uid == slot_id)
                )
                return result.scalar_one_or_none()
        except Exception as e:
            raise DomainException(str(e))
    
    async def create_slot(self, slot: Slot) -> Slot:
        try:
            async with AsyncSessionLocal() as session:
                model = SlotModel(
                    id = slot.id,
                    branch_id = slot.branch_id,
                    service_type_id = slot.service_type_id,
                    staff_id = None if slot.staff_id == "" else int(slot.staff_id) if slot.staff_id else None,
                    start_time = slot.start_time,
                    end_time = slot.end_time,
                    capacity = slot.capacity,
                    is_active = slot.is_active,
                    is_booked = slot.is_booked
                )
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return Slot(
                    id=model.id,
                    branch_id=model.branch_id,
                    service_type_id=model.service_type_id,
                    staff_id=model.staff_id,
                    start_time=model.start_time,
                    end_time=model.end_time,
                    is_booked=model.is_booked,
                    capacity=model.capacity,
                    is_active=model.is_active
                )
        except Exception as e:
            raise DomainException(str(e))
    
    async def update_slot(self, slot_id: str, slot: SlotUpdateDTO) -> Slot:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(SlotModel).where(SlotModel.uid == slot_id))
                model = result.scalar_one_or_none()
                if model:
                    if slot.branch_id is not None:
                        model.branch_id = slot.branch_id
                    if slot.service_type_id is not None:
                        model.service_type_id = slot.service_type_id
                    if slot.staff_id is not None:
                        model.staff_id = None if slot.staff_id == "" else int(slot.staff_id)
                    if slot.start_time is not None:
                        model.start_time = slot.start_time
                    if slot.end_time is not None:
                        model.end_time = slot.end_time
                    if slot.capacity is not None:
                        model.capacity = slot.capacity
                    if slot.is_active is not None:
                        model.is_active = slot.is_active
                        
                    await session.commit()
                    await session.refresh(model)
                    return Slot(
                        id=model.id,
                        branch_id=model.branch_id,
                        service_type_id=model.service_type_id,
                        staff_id=model.staff_id,
                        start_time=model.start_time,
                        end_time=model.end_time,
                        is_booked=model.is_booked,
                        capacity=model.capacity,
                        is_active=model.is_active
                    )
                return None
        except Exception as e:
            raise DomainException(str(e))
    
    async def delete_slot(self, slot_id: UUID)-> None:
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(
                    delete(SlotModel)
                    .where(SlotModel.uid == slot_id)
                )
                await session.commit()
                return None
        except Exception as e:
            raise DomainException(str(e))

    async def count_by_branch_id(self, branch_id: str, service_type_id: str) -> int:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(func.count(SlotModel.id))
                    .where(SlotModel.branch_id == branch_id)
                    .where(SlotModel.service_type_id == service_type_id)
                )
                return result.scalar_one_or_none()
        except Exception as e:
            raise DomainException(str(e))