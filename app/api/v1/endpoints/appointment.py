"""Appointment endpoints."""

from __future__ import annotations

from app.common import *
from app.api.v1.schemas import *
from app.api.v1.schemas.appointment_schemas import *
from app.application.dtos import *

from app.api.middleware.Rbac import get_current_user, require_roles


router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get("/appointments/me")
async def get_my_appointment(
    current_user=Depends(require_roles("CUSTOMER"))
) -> dict:
    return {"user_id": str(current_user.id), "appointments": []}

@router.post(
    "/create",
    response_model=CreateAppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    request: CreateAppointmentRequest,
    current_user= Depends(require_roles("CUSTOMER"))
):  
    dto = AppointmentDTO(
        customer_id=current_user.id,
        branch_id=request.branch_id,
        service_type_id=request.service_type_id,
        staff_id=request.staff_id,
        slot_id=request.slot_id,
        attachment_path=request.attachment_path,
    )
    return CreateAppointmentResponse(
        status="success",
        message="Appointment created successfully",
        data={
            "branch_id": "test",
            "service_type_id": "test",
            "staff_id": "test",
            "start_time": "test",
            "end_time": "test",
            "capacity": 1,
            "is_active": True,
        },
    )


@router.post(
    "/cancel",
    response_model=CancelAppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(payload: CancelAppointmentRequest):

    return CancelAppointmentResponse(
        status="success",
        message="Appointment cancelled successfully",
        data={
            "branch_id": "test",
            "service_type_id": "test",
            "staff_id": "test",
            "start_time": "test",
            "end_time": "test",
            "capacity": 1,
            "is_active": True,
        },
    )


@router.patch(
    "/update",
    response_model=CreateAppointmentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_appointment(payload: UpdateAppointmentRequest):
    return CreateAppointmentResponse(
        status="success",
        message="Your appointment updated successfully",
        data={
            "branch_id": "test",
            "service_type_id": "test",
            "staff_id": "test",
            "start_time": "test",
            "end_time": "test",
            "capacity": 1,
            "is_active": True,
        },
    )
