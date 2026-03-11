from __future__ import annotations

from dataclasses import dataclass

from app.application.dtos.branch_dto import CreateBranchDTO
from app.domain.entities.branch import Branch
from app.domain.interfaces.branch_repository import BranchRepository
import uuid

class BranchUseCase:
    def __init__(self, branch_repository: BranchRepository):
        self.branch_repository = branch_repository

    async def execute(self, request: CreateBranchDTO) -> Branch:
        branch = Branch(
            id=f"br_{uuid.uuid4().hex[:8]}",
            name=request.name,
            city=request.city,
            address=request.address,
            phone=request.phone,
            timezone=request.timezone or "UTC",
            is_active=request.is_active,
        )
        await self.branch_repository.save_branch(branch)
        return branch
