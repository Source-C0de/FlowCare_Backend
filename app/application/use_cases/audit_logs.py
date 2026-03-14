from __future__ import annotations

from app.common import DomainException
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.application.dtos.audit_dto import AuditLogsRequest

class AuditLogsUseCase:
    def __init__(self, audit_logs_repo: AuditLogsRepository):
        self._repo = audit_logs_repo

    async def get_logs(self, request: AuditLogsRequest):
        try:
            result = await self._repo.get_logs(request)
            if result is None:
                return {
                    "data": [],
                    "total": 0,
                    "page": request.page,
                    "limit": request.limit
                }
            return result
        except Exception as e:
            raise DomainException(str(e))
    
    async def export_logs(self, request: AuditLogsRequest):
        try:
            return await self._repo.export_logs(request)
        except Exception as e:
            raise DomainException(str(e))   






__all__ = [
    "AuditLogsUseCase"
]