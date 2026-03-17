from __future__ import annotations

from app.common import dataclass, Dict, List
from uuid import UUID
import uuid

@dataclass
class AuditLog:
    action: str
    actor_id: UUID
    actor_role: str
    entity_id: UUID
    entity_type: str
    branch_id: str | None
    metadata: dict


@dataclass
class AuditLogsResponse:
    data: List[AuditLog]
    total: int
    page: int
    limit: int


@dataclass
class AuditLogsRequest:
    page: int
    limit: int
    term: str | None