"""Branch endpoints."""

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_branch_use_case
from app.api.middleware.rbac import require_roles
from app.api.v1.schemas.branch_schemas import CreateBranchRequest
from app.application.dtos.branch_dto import CreateBranchDTO
from app.application.use_cases.branch import BranchUseCase

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_branch(
    request: CreateBranchRequest,
    use_case: BranchUseCase = Depends(get_branch_use_case),
    current_user=Depends(require_roles("ADMIN")),
):
    dto = CreateBranchDTO(
        name=request.name,
        city=request.city,
        address=request.address,
        phone=request.phone,
        timezone=request.timezone,
        is_active=True,
    )
    branch = await use_case.execute(dto)
    return {"message": "Branch created successfully", "id": branch.id}