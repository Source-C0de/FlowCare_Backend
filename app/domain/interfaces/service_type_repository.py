from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.domain.entities.service_type import ServiceType

@dataclass
class ServiceTypeRepository(ABC):
    @abstractmethod
    def get_service_types(self) -> list[ServiceType]:
        pass

    @abstractmethod
    def get_service_type(self, service_type_id: str) -> ServiceType:
        pass

    @abstractmethod
    def create_service_type(self, service_type: ServiceType) -> ServiceType:
        ...

    @abstractmethod
    def update_service_type(self, service_type_id: str, service_type: ServiceType) -> ServiceType:
        pass

    @abstractmethod
    def delete_service_type(self, service_type_id: str) -> ServiceType:
        ...    
    @abstractmethod
    def count_by_branch_id(self, branch_id: str) -> int:
        ...