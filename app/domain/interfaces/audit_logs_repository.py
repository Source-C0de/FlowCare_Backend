from __future__ import annotations

from abc import ABC, abstractmethod
from app.domain.entities.audit_logs import AuditLogsRequest

class AuditLogsRepository(ABC):
    async def get_logs(self, request: AuditLogsRequest):
      pass
    
    async def export_logs(self):
        pass