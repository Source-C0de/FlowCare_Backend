from __future__ import annotations

import uuid

from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.domain.entities.service_type import ServiceType
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.service_type_model import ServiceType as ServiceTypeModel
from app.domain.exceptions import DomainException
from sqlalchemy import select
from sqlalchemy.sql import func
from app.application.dtos import PaginationDTO

class ServiceTypeRepositoryImpl(ServiceTypeRepository):
    def __init__(self):
        pass

    def _to_entity(self, model: ServiceTypeModel) -> ServiceType:
        return ServiceType(
            id=model.id, 
            branch_id=model.branch_id,
            name=model.name,
            description=model.description,
            duration_minutes=model.duration_minutes,
        )

    async def get_service_types(self,branch_id: str, pagination: PaginationDTO)-> list[ServiceType]:
        try:
            async with AsyncSessionLocal() as session:
                query = select(ServiceTypeModel).where(
                    ServiceTypeModel.branch_id == branch_id,
                    ServiceTypeModel.is_active == True
                )
                if pagination:
                    query = query.offset(pagination.offset).limit(pagination.limit)
                result = await session.execute(query)
                models = result.scalars().all()
                return [self._to_entity(m) for m in models]
        except Exception as exc:
            raise DomainException(str(exc))

    async def get_service_type(self, service_type_id: uuid.UUID)-> ServiceType:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(ServiceTypeModel.uid == service_type_id))
                model = result.scalar_one_or_none()
                if model:
                    return ServiceType(
                        id=model.id, branch_id=model.branch_id, name=model.name,
                        description=model.description,duration_minutes=model.duration_minutes,
                        is_active=model.is_active
                    )
                return None
        except Exception as exc:
            raise DomainException(str(exc))

    async def create_service_type(self, public_id: str, service_type: ServiceType)-> ServiceType:
        try:
            async with AsyncSessionLocal() as session:
                model = ServiceTypeModel(
                    id = public_id,
                    name = service_type.name,
                    branch_id = service_type.branch_id,
                    description = service_type.description,
                    duration_minutes = service_type.duration_minutes,
                    is_active = True
                )
                session.add(model)
                await session.commit()
                return self._to_entity(model)
        except Exception as exc:
            raise DomainException(str(exc))

    async def update_service_type(self, service_type_id: str, service_type: ServiceType)-> ServiceType:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(
                    ServiceTypeModel.id == service_type.id,
                    ServiceTypeModel.is_active == True  
                ))
                model = result.scalar_one_or_none()
                if model:
                    if service_type.name:
                        model.name = service_type.name
                    if service_type.description:
                        model.description = service_type.description
                    if service_type.duration_minutes:
                        model.duration_minutes = service_type.duration_minutes
                    if service_type.is_active:
                        model.is_active = service_type.is_active
                await session.commit()
                await session.refresh(model)
                return self._to_entity(model)

        except Exception as exc:
            raise DomainException(str(exc))

    async def delete_service_type(self, service_type_id: uuid) -> None:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(ServiceTypeModel.uid == service_type_id))
                model = result.scalar_one_or_none()
                if model:
                    await session.delete(model)
                    await session.commit()
                    return
                return None
        except Exception as exc:
            raise DomainException(str(exc))

    async def count_by_branch_id(self, branch_id: str) -> int:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(func.count(ServiceTypeModel.id)).where(ServiceTypeModel.branch_id == branch_id))
                return result.scalar() or 0
        except Exception as exc:

            raise DomainException(str(exc))