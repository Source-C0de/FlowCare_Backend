from __future__ import annotations

from app.common import APIRouter,Depends,status,HTTPException

from app.api.v1.schemas.slot_schemas import (
    GetSlotsRequest,
    CreateSlotRequest,
    UpdateSlotRequest,
    DeleteSlotRequest
)
from app.application.use_cases.slots import SlotUseCase
from app.api.dependencies import get_slot_use_case
from app.application.dtos.slot_dto import SlotDTO, SlotUpdateDTO
from app.api.middleware.Rbac import require_roles
from app.domain.entities.user import User
from uuid import UUID



router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/")
async def get_slots(
    request: GetSlotsRequest = Depends(),
    use_case: SlotUseCase = Depends(get_slot_use_case)
):
    result = await use_case.get_slots(request)
    return {"message": "Slots fatched successfully", "data": result}


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_slot(
    request: CreateSlotRequest,
    use_case: SlotUseCase = Depends(get_slot_use_case),
    current_user= Depends(require_roles("ADMIN","BRANCH_MANAGER"))
):
    user, role = current_user
    if role == "BRANCH_MANAGER":
        if user.branch_id != request.branch_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to create slot in this branch")
    dto = SlotDTO(
        branch_id=request.branch_id,
        service_type_id=request.service_type_id,
        staff_id=request.staff_id,
        start_time=request.start_at,
        end_time=request.end_at,
        capacity=request.capacity,
        is_active=request.is_active,
        is_booked=False,
    )

    result = await use_case.create_slot(dto)
    return {"message": "Slot created successfully", "data": result}


@router.patch("/{slot_id}")
async def update_slot(
    request: UpdateSlotRequest,
    use_case: SlotUseCase = Depends(get_slot_use_case),
    current_user: User = Depends(require_roles(["ADMIN", "BRANCH_MANAGER"]))
):
    user, role = current_user
    if role == "BRANCH_MANAGER":
        if user.branch_id != request.branch_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update slot in this branch")
            
    dto = SlotUpdateDTO(
        id=slot_id,
        branch_id=request.branch_id,
        service_type_id=request.service_type_id,
        staff_id=request.staff_id,
        start_time=request.start_at,
        end_time=request.end_at,
        capacity=request.capacity,
        is_active=request.is_active,
        is_booked=None
    )
    result = await use_case.update_slot(slot_id, dto)
    return {"message": "Slot updated successfully", "data": result}


@router.delete("/{slot_id}")
async def delete_slot(
    slot_id: UUID,
    user_case: SlotUseCase = Depends(get_slot_use_case),
    current_user = Depends(require_roles("ADMIN","BRANCH_MANAGER"))
):
    user, role = current_user
    if role == "BRANCH_MANAGER":
        if user.branch_id != slot_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete slot in this branch")
    result = await user_case.delete_slot(slot_id)
    return result
