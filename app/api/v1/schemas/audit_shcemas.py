from __future__ import annotations

from app.common import BaseModel


class AuditLogsRequest(BaseModel):
    page: int
    limit: int
    offset: int | None = None

class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity: str
    entity_id: str
    user_id: str
    timestamp: str
    details: dict

class PaginatedResponse(BaseModel):
    data: list[AuditLogResponse]
    total: int
    page: int
    limit: int


__all__ = [
    "AuditLogsRequest",
    "AuditLogResponse",
    "PaginatedResponse",
]
