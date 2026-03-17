from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.domain.entities.service_type import ServiceType
from app.api.v1.schemas import *
from app.application.dtos import * 
from app.infrastructure.utils.pagination import PaginationRequest


@dataclass
class ServiceTypeRepository(ABC):
    @abstractmethod
    def get_service_types(self, branch_id: str, pagination: PaginationDTO) -> list[ServiceType]:
        pass

    @abstractmethod
    def get_service_type(self, service_type_id: str) -> ServiceType:
        ...

    @abstractmethod
    def create_service_type(self, public_id: str,service_type: ServiceType) -> ServiceType:
        ...

    @abstractmethod
    def update_service_type(self, service_type_id: str, service_type: ServiceType) -> ServiceType:
        ...

    @abstractmethod
    def delete_service_type(self, service_type_id: uuid.UUID) -> None:
        ...    
    @abstractmethod
    def count_by_branch_id(self, branch_id: str) -> int:
        ...