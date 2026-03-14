from __future__ import annotations

from app.common import BaseModel,dataclass

@dataclass
class AuditLogs:
    id: int
    action: str
    entity: str
    entity_id: str
    user_id: str
    timestamp: str
    details: dict


@dataclass
class AuditLogsResponse:
    data: list[AuditLogs]
    total: int
    page: int
    limit: int


@dataclass
class AuditLogsRequest:
    page: int
    limit: int
    term: int | None