from __future__ import annotations

from typing import Optional

from app.domain.entities.branch import Branch
from app.domain.exceptions import DomainException
from app.domain.interfaces.branch_repository import BranchRepository
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.branch_model import Branch as BranchModel


class BranchRepositoryImpl(BranchRepository):
    async def save_branch(self, branch: Branch) -> None:
        try:
            async with AsyncSessionLocal() as session:
                print(branch)
                branch_model = BranchModel(
                    id=branch.id,
                    name=branch.name,
                    city=branch.city,
                    address=branch.address,
                    phone=branch.phone,
                    timezone=branch.timezone,
                    is_active=branch.is_active
                )
                session.add(branch_model)
                await session.commit()
        except Exception as exc:
            raise DomainException(str(exc))

    async def find_by_id(self, branch_id: str) -> Optional[Branch]:
        pass

    async def find_by_name(self, branch_name: str) -> Optional[Branch]:
        pass

    async def find_all(self) -> list[Branch]:
        return []

    async def update_branch(self, branch: Branch) -> None:
        pass

    async def delete_branch(self, branch_id: str) -> None:
        pass