"""Appointment endpoints."""

from __future__ import annotations

from app.common import APIRouter, Depends, HTTPException, status

from app.api.middleware.Rbac import get_current_user
from app.api.v1.schemas.appointment_schemas import (
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    CreateAppointmentRequest,
    CreateAppointmentResponse,
    UpdateAppointmentRequest,
)

router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get("/appointments/me")
async def get_my_appointment(
    current_user=Depends(get_current_user),
) -> dict:
    user, role = current_user
    if role != "CUSTOMER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return {"user_id": str(user.id), "appointments": []}


@router.post(
    "/create-appointment",
    response_model=CreateAppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    payload: CreateAppointmentRequest,
    current_user=Depends(get_current_user),
):
    user, role = current_user
    if role != "CUSTOMER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
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
    "/cancel-appointment",
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
    "/update_appointment",
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
