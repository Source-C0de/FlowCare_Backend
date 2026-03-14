from __future__ import annotations

from app.common import APIRouter,Depends,status,HTTPException,pagination_params,PaginationRequest

from fastapi.responses import StreamingResponse
from app.api.dependencies import get_audit_use_case
from app.application.use_cases.audit_logs import AuditLogsUseCase
from app.api.middleware.Rbac import require_roles
from app.api.v1.schemas.audit_shcemas import (
    AuditLogsRequest,
    AuditLogResponse,
    PaginatedResponse,
)


router = APIRouter(prefix="/audit", tags=["Audit"], dependencies=[Depends(require_roles("ADMIN"))])


@router.get("/logs")
async def get_logs(
    use_case: AuditLogsUseCase = Depends(get_audit_use_case),
):
    request = AuditLogsRequest(
        page = 1,
        limit = 10000
    )
    result = await use_case.get_logs(request)
    return {"message": "Logs fatched successfully", "data": result}


@router.get("/logs/export",response_class=StreamingResponse)
async def export_logs(
    # request: PaginationRequest = Depends(pagination_params),
    use_case: AuditLogsUseCase = Depends(get_audit_use_case)
):
    request = AuditLogsRequest(
        page = 1,
        limit = 1000,
        offset = 0
    )
    result = await use_case.export_logs(request)
    return {
        "message": "Logs exported successfully",
        "data": "result"
    }
