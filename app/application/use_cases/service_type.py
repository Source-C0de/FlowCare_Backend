from __future__ import annotations

from app.common import DomainException
from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.application.dtos.service_type_dto import ServiceTypeDTO
from app.domain.entities.service_type import ServiceType
from app.infrastructure.utils.utils import generate_service_type_public_id
from app.application.dtos import *



class ServiceTypeUseCase:
    def __init__(self, service_type_repository: ServiceTypeRepository):
        self.service_type_repository = service_type_repository

    async def get_all_service_types(self, branch_id: str, pagination: PaginationDTO):
        return await self.service_type_repository.get_service_types(branch_id, pagination)

    async def get_service_type(self, service_type_id: str):
        return await self.service_type_repository.get_service_type(service_type_id)

    async def create_service_type(self, current_user: User, service_type: ServiceTypeDTO)-> ServiceType:
        try:
            user, role = current_user
            if role != "ADMIN" and user.branch_id != service_type.branch_id:
                raise DomainException("You are not authorized to create service type for this branch")
            
            count = await self.service_type_repository.count_by_branch_id(service_type.branch_id)
            if count is None:
                count = 0
            public_id = generate_service_type_public_id(service_type.branch_id, count + 1) 
            return await self.service_type_repository.create_service_type(public_id, service_type)
        except Exception as e:
            raise DomainException(str(e))

    async def update_service_type(self, current_user: User, service_type: ServiceTypeUpdateDTO):
        try:
            user, role = current_user
            if role != "ADMIN" and user.branch_id != service_type.branch_id:
                raise DomainException("You are not authorized to update service type for this branch")

            if service_type.branch_id != user.branch_id:
                raise DomainException("You are not authorized to update service type for this branch")
            
            check_service_availibility = await self.service_type_repository.get_service_type(service_type.service_type_id)
            if check_service_availibility is None:
                raise DomainException("Service Not Found")

            
            return await self.service_type_repository.update_service_type(service_type)
        except Exception as e:
            raise DomainException(str(e))

    async def delete_service_type(self, service_type_id: uuid.UUID):
        try:
            service_type = await self.service_type_repository.get_service_type(service_type_id)
            if service_type is None:
                return {
                    "message": "Service Not Found"
                }
            result = await self.service_type_repository.delete_service_type(service_type_id)
            if result is None:
                return {
                    "message": "Service Deleted Successfully"+str(service_type_id)
                }
            return result
        except Exception as e:
            raise DomainException(str(e))




__all__ = [
    "ServiceTypeUseCase"
]