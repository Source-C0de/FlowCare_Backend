from __future__ import annotations

from dataclasses import dataclass
from app.domain.exceptions import DomainException
from app.application.dtos.branch_dto import CreateBranchDTO
from app.domain.entities.branch import Branch
from app.domain.interfaces.branch_repository import BranchRepository
import uuid
from app.infrastructure.utils.utils import generate_branch_public_id

class BranchUseCase:
    def __init__(self, branch_repository: BranchRepository):
        self.branch_repository = branch_repository

    async def execute(self, request: CreateBranchDTO) -> Branch:
        count = await self.branch_repository.count_by_city(request.city)
        if count is None:
            count = 0
        public_id = generate_branch_public_id(request.city, count + 1)
        branch = Branch(
            id=public_id,
            name=request.name,
            city=request.city,
            address=request.address,
            phone=request.phone,
            timezone=request.timezone or "UTC",
            is_active=request.is_active,
        )
        await self.branch_repository.save_branch(branch)
        return branch

    async def update_branch(self, branch_id: str, request: CreateBranchDTO) -> Branch:
        branch = await self.branch_repository.find_by_id(branch_id)
        if branch is None:
            raise DomainException("Branch not found")
            
        branch.name = request.name
        branch.city = request.city
        branch.address = request.address
        branch.phone = request.phone
        branch.timezone = request.timezone
        branch.is_active = request.is_active
        await self.branch_repository.update_branch(branch)
        return branch

    async def find_all(self):
        return await self.branch_repository.find_all()

    async def delete_branch(self, branch_id: str) -> None:
        branch = await self.branch_repository.find_by_id(branch_id)
        if branch is None:
            raise DomainException("Branch not found")
        await self.branch_repository.delete_branch(branch_id)