"""Branch endpoints."""

from app.common import *
from app.api.v1.schemas import *
from app.application.use_cases import *
from app.application.dtos import *

from app.api.dependencies import get_branch_use_case
from app.api.middleware.Rbac import require_roles
from app.infrastructure.utils.pagination import PaginationRequest


router = APIRouter(prefix="/branches", tags=["Branches"])


# --Public: Get All Branches--
@router.get("/", response_model=PaginationResponse[BranchDetails], status_code=status.HTTP_200_OK)
async def get_all_branches(
    pagination: PaginationRequest = Depends(PaginationRequest),
    use_case: BranchUseCase = Depends(get_branch_use_case),
):
    branches = await use_case.find_all(pagination)
    return PaginationResponse(
        data=branches,
        total=len(branches),
        page=pagination.page,
        limit=pagination.limit,
    )


# --Private: Create Branch--
@router.post(
    "/", 
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED)
async def create_branch(
    request: CreateBranchRequest = Depends(CreateBranchRequest),
    use_case: BranchUseCase = Depends(get_branch_use_case),
    current_user=Depends(require_roles("ADMIN")),
):
    dto = CreateBranchDTO(
        name=request.name,
        city=request.city,
        address=request.address,
        phone=request.phone,
        timezone=request.timezone,
    )
    branch = await use_case.execute(dto)
    return BranchResponse(
        status="success",
        message="Branch created successfully",
        data=branch,
    )


# --Private: Update Branch--
@router.patch(
    "/{branch_id}", 
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK
)
async def update_branch(
    branch_id: str,
    request: UpdateBranchRequest = Depends(UpdateBranchRequest),
    use_case: BranchUseCase = Depends(get_branch_use_case),
    current_user=Depends(require_roles("ADMIN")),
):
    dto = UpdateBranchDTO(
        name=request.name,
        city=request.city,
        address=request.address,
        phone=request.phone,
        timezone=request.timezone,
        is_active=request.is_active,
    )
    branch = await use_case.update_branch(branch_id, dto)
    return UpdateBranchResponse(
        status="success",
        message="Branch updated successfully",
        data=branch,
    )

# --Private: Delete Branch--
@router.delete("/{branch_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(
    branch_id: str,
    use_case: BranchUseCase = Depends(get_branch_use_case),
    current_user=Depends(require_roles("ADMIN")),
):
    await use_case.delete_branch(branch_id)
    return {"message": "Branch deleted successfully"}