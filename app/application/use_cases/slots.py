from __future__ import annotations

from app.domain.interfaces.slot_repository import SlotRepository


class SlotUseCase:
    def __init__(self, slot_repository: SlotRepository):
        self.slot_repository = slot_repository

    async def get_slots(self, dto: SlotDTO):
        return await self.slot_repository.get_slots(dto)
        
    async def create_slot(self, slot: SlotDTO):
        return await self.slot_repository.create_slot(slot)
    
    async def update_slot(self, slot_id: str, slot: SlotDTO):
        return await self.slot_repository.update_slot(slot_id, slot)
    
    async def delete_slot(self, slot_id: str):
        return await self.slot_repository.delete_slot(slot_id)