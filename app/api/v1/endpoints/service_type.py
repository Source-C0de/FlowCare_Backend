"""Service type endpoints."""

from app.common import *
from app.api.v1.schemas import *
from app.application.use_cases import *

from app.api.dependencies import get_service_type_use_case
from app.api.middleware.Rbac import require_roles

router = APIRouter(prefix="/service-types", tags=["Service Types"])


@router.get("/")
async def get_service_types(
    use_case = Depends(get_service_type_use_case)
):
    result = await use_case.get_service_types()
    return result
    # return GetServiceTypeResponse(
    #     status="success",
    #     message="Service types fetched successfully",
    #     data=result,
    # )

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_service_type(
    request: CreateServiceTypeRequest,
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN")),
):
    dto = ServiceTypeDTO(
        name=request.name,
        branch_id=request.branch_id,
        description=request.description,
        duration_minutes=request.duration_minutes,
        is_active=True,
    )
    result = await use_case.create_service_type(dto)
    return {"message": "Service type created successfully", "data": result}

@router.patch("/{service_type_id}")
async def update_service_type(
    service_type_id: uuid.UUID,
    request: UpdateServiceTypeRequest,
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN"))
):
    dto = ServiceTypeUpdateDTO(
        id=request.id,
        name=request.name,
        branch_id=request.branch_id,
        description=request.description,
        duration_minutes=request.duration_minutes,
        is_active=request.is_active,
    )
    result = await use_case.update_service_type(service_type_id,dto)
    return result

@router.delete("/{service_type_id}")
async def delete_service_type(
    service_type_id: uuid.UUID,
    use_case: ServiceTypeUseCase = Depends(get_service_type_use_case),
    current_user=Depends(require_roles("ADMIN"))
):
    result = await use_case.delete_service_type(service_type_id)
    return result



