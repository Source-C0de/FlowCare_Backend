from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.branch import Branch
from app.application.dtos import PaginationDTO, UpdateBranchDTO
# from app.infrastructure.repositories.branch_repository_impl import BranchRepositoryImpl

class BranchRepository(ABC):
    @abstractmethod
    async def save_branch(self, public_id: str, branch: Branch) -> None:
        ...

    @abstractmethod
    async def find_by_id(self, branch_id: str) -> Optional[Branch]:
        pass

    @abstractmethod
    async def find_by_name(self, branch_name: str) -> Optional[Branch]:
        pass

    @abstractmethod
    async def find_all(self, pagination: PaginationDTO) -> list[Branch]:
        ...

    @abstractmethod
    async def update_branch(self, branch_id: str, request: UpdateBranchDTO) -> None:
        ...

    @abstractmethod
    async def delete_branch(self, branch_id: str) -> None:
        pass

    @abstractmethod
    async def count_by_city(self, city: str) -> int:
        ...

    @abstractmethod
    async def find_by_phone(self, phone: str) -> bool:
        pass