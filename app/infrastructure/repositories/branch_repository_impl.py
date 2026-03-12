from __future__ import annotations

from typing import Optional
from fastapi import Depends
from sqlalchemy import select, func, delete




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
            model = result.scalar_one_or_none()
            if model:
                return Branch(
                    id=model.id,
                    name=model.name,
                    city=model.city,
                    address=model.address,
                    phone=model.phone,
                    timezone=model.timezone,
                    is_active=model.is_active
                )
            return None

    async def find_by_name(self, branch_name: str) -> Optional[Branch]:
        pass

    async def find_all(self) -> list[Branch]:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(BranchModel))
                models = result.scalars().all()
                return [
                    Branch(
                        id=m.id, name=m.name, city=m.city, address=m.address,
                        phone=m.phone, timezone=m.timezone, is_active=m.is_active
                    ) for m in models
                ]
        except Exception as exc:
            raise DomainException(str(exc))

    async def update_branch(self, branch: Branch) -> None:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(BranchModel).where(BranchModel.id == branch.id))
                model = result.scalar_one()
                model.name = branch.name
                model.city = branch.city
                model.address = branch.address
                model.phone = branch.phone
                model.timezone = branch.timezone
                model.is_active = branch.is_active
                await session.commit()
        except Exception as exc:
            raise DomainException(str(exc))

    async def delete_branch(self, branch_id: str) -> None:
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(delete(BranchModel).where(BranchModel.id == branch_id))
                await session.commit()
        except Exception as exc:
            raise DomainException(str(exc))

    async def count_by_city(self, city: str) -> int:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(BranchModel.id)).where(BranchModel.city == city))
            return result.scalar() or 0