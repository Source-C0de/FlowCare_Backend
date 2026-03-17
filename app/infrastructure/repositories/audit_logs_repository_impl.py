from __future__ import annotations

from app.common import *
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.domain.entities.audit_logs import AuditLogsRequest, AuditLog
from app.infrastructure.models.audit_log_model import AuditLog as AuditLogsModel
from app.infrastructure.database.session import AsyncSessionLocal
from sqlalchemy import select
from fastapi.responses import StreamingResponse
import csv
import io
from uuid import uuid4, UUID

class AuditLogsRepositoryImpl(AuditLogsRepository):
    def __init__(self):
        pass
    
    async def create_logs(self, request: AuditLogsRequest):
        try:
            async with AsyncSessionLocal() as session:
                lgo = AuditLogsModel(
                    uid=uuid4(),
                    id=str(uuid4()),
                    action_type=getattr(request, "action", "unknown"),
                    actor_id=getattr(request, "actor_id", None),
                    actor_role=getattr(request, "actor_role", "unknown"),
                    entity_type=getattr(request, "entity_type", "unknown"),
                    entity_id=getattr(request, "entity_id", None),
                    branch_id=getattr(request, "branch_id", None),
                    log_metadata=getattr(request, "metadata", None) or {},
                )
                session.add(lgo)
                await session.commit()
                return lgo
        except Exception as e:
            raise DomainException(str(e))
    
    async def get_logs(self, request: AuditLogsRequest):
        try:
            async with AsyncSessionLocal() as session:
                query = select(AuditLogsModel)
                query = query.offset((request.page-1)* request.limit).limit(request.limit)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            raise DomainException(str(e))
    
    async def export_logs(self, request: AuditLogsRequest):
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["id", "action_type", "actor_id", "actor_role", "entity_type", "entity_id", "metadata", "created_at", "updated_at"])
            logs = await self.get_logs(request)
            for log in logs:
                writer.writerow([log.id, log.action_type, log.actor_id, log.actor_role, log.entity_type, log.entity_id, log.log_metadata, log.created_at.isoformat(), log.updated_at.isoformat()])
            output.seek(0)

            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=audit_logs.csv"},
            )   

        except Exception as e:
            raise DomainException(str(e))

    async def write_audit_log(self, audit_log: AuditLog) -> None:     
        async with AsyncSessionLocal() as session:
            model = AuditLogsModel(
                uid=uuid4(),
                id=str(uuid4()),
                action_type=audit_log.action,
                actor_id=audit_log.actor_id,
                actor_role=audit_log.actor_role,
                entity_id=audit_log.entity_id,
                entity_type=audit_log.entity_type,
                branch_id=audit_log.branch_id,
                log_metadata=audit_log.metadata,
            )
            session.add(model)
            await session.commit()