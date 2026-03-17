"""Service type endpoints."""

from app.common import *
from app.api.v1.schemas import *
from app.application.use_cases import *
from app.application.dtos import *

from app.api.dependencies import get_service_type_use_case
from app.api.middleware.Rbac import require_roles
from app.infrastructure.utils.pagination import PaginationRequest, pagination_params
router = APIRouter(prefix="/service-types", tags=["Service Types"])



# --Public: Get All Service Types--
@router.get(
    "/branches/{branch_id}", 
    response_model=PaginationResponse[ServiceType],
    status_code=status.HTTP_200_OK
)
async def get_service_types(
    branch_id: str, 
    pagination: PaginationRequest = Depends(pagination_params),
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case)
):
    result = await use_case.get_all_service_types(branch_id, pagination)
    return PaginationResponse(
        data=result,
        total=len(result),
        page=pagination.page,
        limit=pagination.limit,
    )


# --Private: Create Service Type--
@router.post(
    "/",
    response_model=ServiceTypeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_service_type(
    branch_id: str,
    request: ServiceTypeRequest = Depends(ServiceTypeRequest),
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN","BRANCH_MANAGER")),
):
    dto = ServiceTypeDTO(
        branch_id=branch_id,
        name=request.name,
        description=request.description,
        duration_minutes=request.duration_minutes,
    )
    result = await use_case.create_service_type(current_user,dto)
    return ServiceTypeResponse(
        status="success",
        message="Service type created successfully",
        data=result,
    )


# --Private: Update Service Type--
@router.patch(
    "/{service_type_id}",
    response_model=UpdateServiceTypeResponse,
    status_code=status.HTTP_200_OK
)
async def update_service_type(
    branch_id: str,
    service_type_id: str,
    request: UpdateServiceTypeRequest = Depends(UpdateServiceTypeRequest),
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN","BRANCH_MANAGER"))
):
    dto = ServiceTypeUpdateDTO(
        branch_id=branch_id,
        service_type_id=service_type_id,
        name=request.name,
        description=request.description,
        duration_minutes=request.duration_minutes,
        is_active=request.is_active,
    )
    result = await use_case.update_service_type(current_user,dto)
    return UpdateServiceTypeResponse(
        status="success",
        message="Service type updated successfully",
        data=result,
    )

@router.delete("/{service_type_id}")
async def delete_service_type(
    service_type_id: uuid.UUID,
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN"))
):
    result = await use_case.delete_service_type(service_type_id)
    return result



