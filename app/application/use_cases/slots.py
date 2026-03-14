from __future__ import annotations

from app.domain.interfaces.slot_repository import SlotRepository
from app.application.dtos.slot_dto import SlotDTO, SlotUpdateDTO
from app.domain.entities.slot import Slot
from app.api.v1.schemas.slot_schemas import GetSlotsRequest
from app.infrastructure.utils.utils import generate_slot_public_id
from app.common import DomainException
from uuid import UUID

class SlotUseCase:
    def __init__(self, slot_repository: SlotRepository):
        self.slot_repository = slot_repository

    async def get_slots(self, slot: GetSlotsRequest): 
        try:
            return await self.slot_repository.get_slots(slot)
        except Exception as e:
            raise DomainException(str(e))
        
    async def create_slot(self, slotData: SlotDTO)->Slot:
        try:
            count = await self.slot_repository.count_by_branch_id(slotData.branch_id, slotData.service_type_id)
            if count is None:
                count = 0
            public_id = generate_slot_public_id(slotData.branch_id,count + 1)
            slot = Slot(
                id=public_id,
                branch_id=slotData.branch_id,
                service_type_id=slotData.service_type_id,
                staff_id=slotData.staff_id,
                start_time=slotData.start_time,
                end_time=slotData.end_time,
                capacity=slotData.capacity,
                is_booked=slotData.is_booked,
                is_active=slotData.is_active,
            )
            # return slot
            return await self.slot_repository.create_slot(slot)
        except Exception as e:
            raise DomainException(str(e))
    
    async def update_slot(self, slot_id: str, slot: SlotUpdateDTO):
        return await self.slot_repository.update_slot(slot_id, slot)
    
    async def delete_slot(self, slot_id: UUID):
        try:
            slot = await self.slot_repository.get_slot_by_id(slot_id)
            if slot is None:
                raise DomainException("Slot not found")
            result = await self.slot_repository.delete_slot(slot_id)
            if result is None:
                return {
                    "message": "Slot deleted successfully"
                }
            else:
                raise DomainException("Failed to delete slot")
        except Exception as e:
            raise DomainException(str(e))

