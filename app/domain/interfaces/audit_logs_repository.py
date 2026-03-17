from __future__ import annotations

from abc import ABC, abstractmethod
from app.domain.entities.audit_logs import AuditLogsRequest, AuditLog
from app.infrastructure.models.audit_log_model import AuditLog as AuditLogModel

class AuditLogsRepository(ABC):
    @abstractmethod
    async def get_logs(self, request: AuditLogsRequest):
      pass
    
    @abstractmethod
    async def export_logs(self):
        pass

    @abstractmethod
    async def write_audit_log(self, audit_log: AuditLog) -> None:
        pass