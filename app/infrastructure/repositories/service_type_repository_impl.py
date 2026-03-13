from __future__ import annotations

from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.domain.entities.service_type import ServiceType
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.service_type_model import ServiceType as ServiceTypeModel
from app.domain.exceptions import DomainException
from sqlalchemy import select
from sqlalchemy.sql import func

class ServiceTypeRepositoryImpl(ServiceTypeRepository):
    def __init__(self):
        pass

    async def get_service_types(self)-> list[ServiceType]:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel))
                models = result.scalars().all()
                return [
                    ServiceType(
                        id=m.id, branch_id=m.branch_id, name=m.name,
                        description=m.description,duration_minutes=m.duration_minutes,
                        is_active=m.is_active
                    ) for m in models
                ]
        except Exception as exc:
            raise DomainException(str(exc))

    async def get_service_type(self, service_type_id: str):
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(ServiceTypeModel.id == service_type_id))
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

    async def create_service_type(self, service_type: ServiceType)-> ServiceType:
        try:
            async with AsyncSessionLocal() as session:
                model = ServiceTypeModel(
                    id = service_type.id,
                    name = service_type.name,
                    branch_id = service_type.branch_id,
                    description = service_type.description,
                    duration_minutes = service_type.duration_minutes,
                    is_active = service_type.is_active
                )
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return ServiceType(
                    id=model.id, branch_id=model.branch_id, name=model.name,
                    description=model.description,duration_minutes=model.duration_minutes,
                    is_active=model.is_active
                )
        except Exception as exc:
            raise DomainException(str(exc))

    async def update_service_type(self, service_type_id: str, service_type: ServiceType):
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(ServiceTypeModel.id == service_type_id))
                model = result.scalar_one_or_none()
                if model:
                    model.name = service_type.name
                    model.branch_id = service_type.branch_id
                    model.description = service_type.description
                    model.duration_minutes = service_type.duration_minutes
                    model.is_active = service_type.is_active
                    await session.commit()
                    await session.refresh(model)
                    return ServiceType(
                        id=model.id, branch_id=model.branch_id, name=model.name,
                        description=model.description,duration_minutes=model.duration_minutes,
                        is_active=model.is_active
                    )
                return None
        except Exception as exc:
            raise DomainException(str(exc))

    async def delete_service_type(self, service_type_id: str):
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(ServiceTypeModel).where(ServiceTypeModel.id == service_type_id))
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