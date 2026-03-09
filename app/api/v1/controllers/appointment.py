from fastapi import APIRouter, status
from typing import Optional, Any



from app.api.v1.schemas.appointment_schema import CreateAppointmentResponse, CreateAppointmentRequest


router = APIRouter(prefix="/appointment", tags=["Appointment"])

@router.post("/create-appointment", response_model=CreateAppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: CreateAppointmentRequest
):
    print(payload)
    return CreateAppointmentResponse(
        status="success",
        message="Appointment created successfully",
        data= {
            "branch_id": "test",
            "service_type_id": "test",
            "staff_id": "test",
            "start_time": "test",
            "end_time": "test",
            "capacity": 1,
            "is_active": True
        }
    )