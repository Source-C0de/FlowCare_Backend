from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User
from app.application.dtos.staff_dto import CreateStaffDTO, StaffUpdateDTO, StaffAssignDTO, StaffPublicDTO
from app.api.v1.schemas.common import PaginationRequest

class StaffRepository(ABC):
    @abstractmethod
    async def find_all(self, pagination: PaginationRequest, branch_id: Optional[str] = None) -> List[User]:
        ...

    @abstractmethod
    async def find_by_id(self, staff_id: int) -> Optional[User]:
        ...

    @abstractmethod
    async def create_staff(self, dto: CreateStaffDTO) -> User:
        ...

    @abstractmethod
    async def update_staff(self, staff_id: int, dto: StaffUpdateDTO) -> User:
        ...

    @abstractmethod
    async def delete_staff(self, staff_id: int) -> bool:
        ...

    @abstractmethod
    async def assign_service(self, dto: StaffAssignDTO) -> StaffServiceType:
        ...

    @abstractmethod
    async def unassign_service(self, dto: StaffAssignDTO) -> Any:
        ...
