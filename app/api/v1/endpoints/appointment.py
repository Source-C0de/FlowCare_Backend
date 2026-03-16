"""Appointment endpoints."""

from __future__ import annotations

from app.common import *
from app.api.v1.schemas import *
from app.application.dtos import *    
from app.application.use_cases import *
from app.api.middleware.Rbac import get_current_user, require_roles
from app.api.dependencies import get_appointment_use_case


router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get("/me", response_model=list[AppointmentDetails])
async def get_my_appointments(
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    appointments = await use_case.get_user_appointments(str(user.id))
    # Map to schemas
    return [
        AppointmentDetails(
            id=str(a.id),
            appointment_no=a.appoinment_no,
            branch_id=a.branch_id,
            service_type_id=a.service_type_id or "",
            staff_id=str(a.staff_id) if a.staff_id else "",
            status=a.status.value,
            slot_id=a.slot_id or "",
            attachment_path=a.attachment_path
        ) for a in appointments
    ]


@router.post(
    "/create",
    response_model=CreateAppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    request: CreateAppointmentRequest = Depends(),
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):  
    user, role = current_user
    dto = AppointmentDTO(
        customer_id=str(user.id),
        branch_id=request.branch_id,
        service_type_id=request.service_type_id,
        staff_id=request.staff_id,
        slot_id=request.slot_id,
        attachment=request.attachment,
    )
    appointment = await use_case.create_appointment(dto)
    return CreateAppointmentResponse(
        status="success",
        message="Appointment created successfully",
        data=AppointmentDetails(
            id=str(appointment.id),
            appointment_no=appointment.appoinment_no,
            branch_id=appointment.branch_id,
            service_type_id=appointment.service_type_id or "",
            staff_id=str(appointment.staff_id) if appointment.staff_id else "",
            status=appointment.status.value,
            slot_id=appointment.slot_id or "",
            attachment_path=appointment.attachment_path
        ),
    )


@router.post(
    "/cancel/{appointment_id}",
    response_model=CancelAppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(
    appointment_id: str,
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    appointment = await use_case.cancel_appointment(appointment_id, str(user.id))

    return CancelAppointmentResponse(
        status="success",
        message="Appointment cancelled successfully",
        data=AppointmentDetails(
            id=str(appointment.id),
            appointment_no=appointment.appoinment_no,
            branch_id=appointment.branch_id,
            service_type_id=appointment.service_type_id or "",
            staff_id=str(appointment.staff_id) if appointment.staff_id else "",
            status=appointment.status.value,
            slot_id=appointment.slot_id or "",
            attachment_path=appointment.attachment_path
        ),
    )


@router.get("/{appointment_id}", response_model=AppointmentDetails)
async def get_appointment_details(
    appointment_id: str,
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    appointment = await use_case.get_appointment_details(appointment_id, str(user.id))
    
    return AppointmentDetails(
        id=str(appointment.id),
        appointment_no=appointment.appoinment_no,
        branch_id=appointment.branch_id,
        service_type_id=appointment.service_type_id or "",
        staff_id=str(appointment.staff_id) if appointment.staff_id else "",
        status=appointment.status.value,
        slot_id=appointment.slot_id or "",
        attachment_path=appointment.attachment_path
    )
