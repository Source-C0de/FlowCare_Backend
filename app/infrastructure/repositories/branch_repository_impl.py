from __future__ import annotations

from typing import Optional
from fastapi import Depends
from sqlalchemy import select, func




from app.domain.entities.branch import Branch
from app.domain.exceptions import DomainException
from app.domain.interfaces.branch_repository import BranchRepository
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.branch_model import Branch as BranchModel


class BranchRepositoryImpl(BranchRepository):
    async def save_branch(self, branch: Branch) -> None:
        try:
            async with AsyncSessionLocal() as session:
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
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(BranchModel).where(BranchModel.id == branch_id)
            )
            return result

    async def find_by_name(self, branch_name: str) -> Optional[Branch]:
        pass

    async def find_all(self) -> list[Branch]:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(BranchModel))
                return result.scalars().all()
        except Exception as exc:
            raise DomainException(str(exc))

    async def update_branch(self, branch: Branch) -> None:
        try:
            for k, v in data.model_dump(exclude_none=True).items():
                setattr(branch, k, v)
            await db.flush()
        except Exception as exc:
            raise DomainException(str(exc))

    async def delete_branch(self, branch_id: str) -> None:
        pass

    async def count_by_city(self, city: str) -> int:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(BranchModel.id)).where(BranchModel.city == city))
            return result.scalar() or 0