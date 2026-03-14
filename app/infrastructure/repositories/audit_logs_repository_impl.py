from __future__ import annotations

from app.common import BaseModel, DomainException,select
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.api.v1.schemas.audit_shcemas import AuditLogsRequest
from app.infrastructure.models.audit_log_model import AuditLog as AuditLogsModel
from app.infrastructure.database.session import AsyncSessionLocal
from sqlalchemy import insert,select,func,delete
from fastapi.responses import StreamingResponse
import csv
import io


class AuditLogsRepositoryImpl(AuditLogsRepository):
    def __init__(self):
        pass
    
    async def create_logs(
        self, request: AuditLogsRequest):
        try:
            async with AsyncSessionLocal() as session:
                lgo = AuditLogsModel(
                    action_type=request.action_type,
                    actor_id=request.actor_id,
                    actor_role=request.actor_role,
                    entity_type=request.entity_type,
                    entity_id=request.entity_id,
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