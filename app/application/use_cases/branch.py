from __future__ import annotations

from dataclasses import dataclass
from app.domain.exceptions import DomainException
from app.domain.entities.branch import Branch
from app.domain.interfaces.branch_repository import BranchRepository
import uuid
from app.infrastructure.utils.utils import generate_branch_public_id

from app.application.dtos import *

class BranchUseCase:
    def __init__(self, branch_repository: BranchRepository):
        self.branch_repository = branch_repository

    async def execute(self, request: CreateBranchDTO) -> Branch:
        _check_phone = await self.branch_repository.find_by_phone(request.phone)
        if _check_phone is True:
            raise DomainException("Phone number already exists")
        count = await self.branch_repository.count_by_city(request.city)
        if count is None:
            count = 0
        public_id = generate_branch_public_id(request.city, count + 1)
            
        return await self.branch_repository.save_branch(public_id,request)

    async def update_branch(self, branch_id: str, request: UpdateBranchDTO) -> Branch:
        if request.phone:
            _check_phone = await self.branch_repository.find_by_phone(request.phone)
            if _check_phone is True:
                raise DomainException("Phone number already exists")

        branch = await self.branch_repository.find_by_id(branch_id)
        if branch is None:
            raise DomainException("Branch not found")
            
        await self.branch_repository.update_branch(branch_id, request)
        return branch

    async def find_all(self, pagination: PaginationDTO):
        return await self.branch_repository.find_all(pagination)

    async def delete_branch(self, branch_id: str) -> None:
        branch = await self.branch_repository.find_by_id(branch_id)
        if branch is None:
            raise DomainException("Branch not found")
        await self.branch_repository.delete_branch(branch_id)




__all__ = [
    "BranchUseCase"
]
