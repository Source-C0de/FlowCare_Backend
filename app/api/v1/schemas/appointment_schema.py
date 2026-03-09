from pydantic import BaseModel
from typing import Optional


class AppointmentDetails(BaseModel):
    branch_id: str
    service_type_id: str
    staff_id: str
    start_time: str
    end_time: str
    capacity: int
    is_active: bool

class CreateAppointmentRequest(BaseModel):
    branch_id: str
    slot_id: str
    service_type_id: str
    staff_id: str
    start_time: str
    end_time: str

class CreateAppointmentResponse(BaseModel):
    status: str
    message: str
    data: AppointmentDetails
