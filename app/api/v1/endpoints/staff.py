from __future__ import annotations

from app.common import *
from app.api.v1.schemas import *
from app.application.dtos import *
from app.application.use_cases import *


from app.api.dependencies import get_staff_use_case 
from app.api.middleware.Rbac import require_roles


from app.config import settings

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get(
    "/", 
    response_model=PaginationResponse[StaffPublic], 
    status_code=status.HTTP_200_OK
)
async def get_all_staff(
    pagination: PaginationRequest = Depends(PaginationRequest),
    use_case: StaffUseCase = Depends(get_staff_use_case),
    current_user = Depends(require_roles("ADMIN", "BRANCH_MANAGER"))
):
    staff = await use_case.find_all(current_user, pagination)
    return PaginationResponse(
        data=staff,
        total=len(staff),
        page=pagination.page,
        limit=pagination.limit,
    )

@router.post(
    "/",
    response_model=StaffPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_staff(
    request: StaffCreate = Depends(StaffCreate),
    use_case: StaffUseCase = Depends(get_staff_use_case),
    current_user = Depends(require_roles("ADMIN", "BRANCH_MANAGER"))
):
    dto = CreateStaffDTO(
        name=request.name,
        email=request.email,
        password=request.password,
        branch_id=request.branch_id,
        role_id=request.role_id,
        phone=request.phone,
    )
    staff = await use_case.create_staff(current_user, dto)
    return staff


@router.patch(
    "/{staff_id}", 
    response_model=StaffPublic, 
    status_code=status.HTTP_200_OK
)
async def update_staff(
    staff_id: int,
    request: StaffUpdate = Depends(StaffUpdate),
    use_case: StaffUseCase = Depends(get_staff_use_case),
    current_user = Depends(require_roles("ADMIN", "BRANCH_MANAGER"))
):
    dto = StaffUpdateDTO(
        name=request.name,
        branch_id=request.branch_id,
        phone=request.phone,
        is_active=request.is_active,
    )
    staff = await use_case.update_staff(current_user,staff_id, dto)
    return staff


@router.post(
    "/{staff_id}/assign-service",
    response_model=StaffAssignResponse,
    status_code=status.HTTP_200_OK
)
async def assign_service(
    staff_id: int,
    request: StaffAssign = Depends(StaffAssign),
    use_case: StaffUseCase = Depends(get_staff_use_case),
    current_user = Depends(require_roles("ADMIN", "BRANCH_MANAGER"))
):
    dto = StaffAssignDTO(
        staff_id=staff_id,
        service_type_id=request.service_type_id,
    )
    staff = await use_case.assign_service(current_user, dto)
    return StaffAssignResponse(
        message="Service assigned successfully",
        staff_id=staff.staff_id,
        service_type_id=staff.service_type_id,
    )


@router.delete(
    "/{staff_id}/unassign-service",
    status_code=status.HTTP_200_OK
)
async def unassign_service(
    staff_id: int,
    request: StaffAssign = Depends(StaffAssign),
    use_case: StaffUseCase = Depends(get_staff_use_case),
    current_user = Depends(require_roles("ADMIN", "BRANCH_MANAGER"))
):
    dto = StaffAssignDTO(
        staff_id=staff_id,
        service_type_id=request.service_type_id,
    )
    await use_case.unassign_service(current_user, dto)
    return {
        "message": "Service unassigned successfully",
        "staff_id": staff_id,
        "service_type_id": request.service_type_id,
    }
