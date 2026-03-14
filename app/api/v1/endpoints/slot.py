from __future__ import annotations

from app.common import APIRouter,Query,Depends

from app.api.v1.schemas.slot_schemas import GetSlotsRequest
from app.application.use_cases.slot import SlotUseCase
from app.api.dependencies import get_slot_use_case
from app.application.dtos.slot_dto import SlotDTO



router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/")
async def get_slots(
    request: GetSlotsRequest,
    use_case: SlotUseCase = Depends(get_slot_use_case)
):
    dto = SlotDTO(
        branch_id=request.branch_id,
        service_type_id=request.service_type_id,
        is_active=request.is_active,
    )
    result = await use_case.get_slots(dto)
    return result


@router.post("/")
async def create_slot():
    return {"message": "Slot created successfully"}


@router.patch("/{slot_id}")
async def update_slot():
    return {"message": "Slot updated successfully"}


@router.delete("/{slot_id}")
async def delete_slot():
    return {"message": "Slot deleted successfully"}
