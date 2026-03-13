from __future__ import annotations

from app.common import DomainException
from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.application.dtos.service_type_dto import ServiceTypeDTO
from app.domain.entities.service_type import ServiceType
from app.infrastructure.utils.utils import generate_service_type_public_id

class ServiceTypeUseCase:
    def __init__(self, service_type_repository: ServiceTypeRepository):
        self.service_type_repository = service_type_repository

    async def get_service_types(self):
        return await self.service_type_repository.get_service_types()

    async def get_service_type(self, service_type_id: str):
        return await self.service_type_repository.get_service_type(service_type_id)

    async def create_service_type(self, service_type: ServiceTypeDTO)-> ServiceType:
        try:
            count = await self.service_type_repository.count_by_branch_id(service_type.branch_id)
            if count is None:
                count = 0
            public_id = generate_service_type_public_id(service_type.branch_id, count + 1) 
            result =  ServiceType(
                id=public_id,
                name=service_type.name,
                branch_id=service_type.branch_id,
                description=service_type.description,
                duration_minutes=service_type.duration_minutes,
                is_active=service_type.is_active,
            )
            return result
            # return await self.service_type_repository.create_service_type(result)
        except Exception as e:
            raise DomainException(str(e))

    async def update_service_type(self, service_type_id: str, service_type: ServiceType):
        return await self.service_type_repository.update_service_type(service_type_id, service_type)

    async def delete_service_type(self, service_type_id: str):
        try:
            return await self.service_type_repository.delete_service_type(service_type_id)
        except Exception as e:
            raise DomainException(str(e))