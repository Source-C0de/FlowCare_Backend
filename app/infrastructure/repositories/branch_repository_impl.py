from __future__ import annotations

from typing import Optional
from fastapi import Depends
from sqlalchemy import select, func, delete

from app.domain.entities.branch import Branch
from app.domain.exceptions import DomainException
from app.domain.interfaces.branch_repository import BranchRepository
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.branch_model import Branch as BranchModel
from app.api.v1.schemas.common import PaginationRequest
from app.domain.entities.branch import UpdateBranch


class BranchRepositoryImpl(BranchRepository):

    def _to_entity(self, model: BranchModel) -> Branch:
        return Branch(
            id=model.id,
            name=model.name,
            city=model.city,
            address=model.address,
            phone=model.phone,
            timezone=model.timezone,
        )

    async def save_branch(self, public_id: str, branch: Branch) -> Branch:
        try:
            async with AsyncSessionLocal() as session:
                branch_model = BranchModel(
                    id=public_id,
                    name=branch.name,
                    city=branch.city,
                    address=branch.address,
                    phone=branch.phone,
                    timezone=branch.timezone,
                    is_active=True
                )
                session.add(branch_model)
                await session.commit()
                return self._to_entity(branch_model)
        except Exception as exc:
            raise DomainException(str(exc))


    async def update_branch(self, branch_id: str, request: UpdateBranch) -> None:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(BranchModel).where(
                    BranchModel.id == branch_id,
                    BranchModel.is_active == True
                ))
                model = result.scalar_one_or_none()
                if request.name:
                    model.name = request.name
                if request.city:
                    model.city = request.city
                if request.address:
                    model.address = request.address
                if request.phone:
                    model.phone = request.phone
                if request.timezone:
                    model.timezone = request.timezone
                if request.is_active:
                    model.is_active = request.is_active

                await session.commit()
                # await session.refresh(model)
                return self._to_entity(model)

        except Exception as exc:
            raise DomainException(str(exc))

    async def find_by_id(self, branch_id: str) -> Optional[Branch]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(BranchModel).where(BranchModel.id == branch_id)
            )
            model = result.scalar_one_or_none()
            if model:
                return self._to_entity(model)
            return None

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

    async def find_by_phone(self, phone: str) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(BranchModel).where(
                BranchModel.phone == phone,
                BranchModel.is_active == True
            ))
            model = result.scalar_one_or_none()
            if model:
                return True
            return False

    async def find_by_name(self, branch_name: str) -> Optional[Branch]:
        pass

    async def find_all(self, pagination: PaginationRequest) -> list[Branch]:
        try:
            async with AsyncSessionLocal() as session:
                query = select(BranchModel).where(BranchModel.is_active == True)
                if pagination:
                    query = query.offset(pagination.offset).limit(pagination.limit)
                result = await session.execute(query)
                models = result.scalars().all()
                return [self._to_entity(m) for m in models]
        except Exception as exc:
            raise DomainException(str(exc))