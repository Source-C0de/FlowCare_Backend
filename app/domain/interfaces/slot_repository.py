from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID
from app.api.v1.schemas.slot_schemas import GetSlotsRequest
from app.application.dtos.slot_dto import SlotDTO, SlotUpdateDTO
from app.api.v1.schemas.common import PaginationRequest

class SlotRepository(ABC):
    @abstractmethod
    async def get_slots(self, request: PaginationRequest, branch_id: str, service_type_id: str, date_filter: Optional[str] = None) -> list[Slot]:
        pass
    
    @abstractmethod
    async def create_slot(self, slot: SlotDTO) -> Slot:
        pass
    
    @abstractmethod
    async def update_slot(self, slot_id: str, slot: SlotUpdateDTO) -> Slot:
        pass
    
    @abstractmethod
    async def delete_slot(self, slot_id: UUID) -> None:
        pass

    @abstractmethod
    async def count_by_branch_id(self, branch_id: str, service_type_id: str) -> int:
        pass

    @abstractmethod
    async def get_slot_by_id(self, slot_id: UUID) -> Slot:
        pass