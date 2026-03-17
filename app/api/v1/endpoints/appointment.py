"""Appointment endpoints."""

from __future__ import annotations

from app.common import *
from app.api.v1.schemas import *
from app.application.dtos import *    
from app.application.use_cases import *
from app.api.middleware.Rbac import get_current_user, require_roles
from app.api.dependencies import get_appointment_use_case


router = APIRouter(prefix="/appointment", tags=["Appointment"])



# --List of My Appointments
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

# --Get Appointment Details--
@router.get("/{appointment_id}", response_model=AppointmentDetails)
async def get_appointment_details(
    appointment_id: str,
    current_user = Depends(get_current_user),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    appointment = await use_case.get_appointment_details(appointment_id, current_user)

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

# --Book Appointment--
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

# --Cancel Appointment--
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


# --Reschedule Appointment--
@router.patch(
    "/update/{appointment_id}",
    response_model=UpdateAppointmentResponse,
    status_code=status.HTTP_200_OK,
)
async def reschedule_appointment(
    appointment_id: str,
    request: UpdateAppointmentRequest = Depends(),
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, _ = current_user
    appointment = await use_case.reschedule_appointment(appointment_id, str(user.id), request.slot_id)
    return UpdateAppointmentResponse(
        status="success",
        message="Appointment updated successfully",
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

# --Admin/Manager/Staff --

@router.get("/all", response_model=PaginationResponse[AppointmentDetails])
async def get_all_appointments(
    pagination: PaginationRequest = Depends(),
    current_user = Depends(require_roles("ADMIN","BRANCH_MANAGER","STAFF")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    branch_id = None
    staff_id = None
    if role == "BRANCH_MANAGER":
        branch_id = user.branch_id
    if role == "STAFF":
        staff_id = user.id
    appointments = await use_case.get_all_appointments(branch_id, staff_id, pagination)
    return PaginationResponse(
        data=[
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
        ],
        total=len(appointments),
        page=pagination.page,
        limit=pagination.limit,
    )


# -- Staff: Update Status---
@router.patch("/status/{appointment_id}", response_model=UpdateAppointmentResponse)
async def update_appointment_status(
    appointment_id: str,
    request: AppointmentStatusUpdate = Depends(),
    current_user = Depends(require_roles("ADMIN","BRANCH_MANAGER","STAFF")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, role = current_user
    branch_id = user.branch_id if role in ("BRANCH_MANAGER","STAFF") else None
    appointment = await use_case.update_appointment_status(appointment_id, request.status, str(user.id), branch_id)
    return UpdateAppointmentResponse(
        status="success",
        message="Appointment status updated successfully",
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




# --Queue Position--
@router.get("/queue/{branch_id}")
async def get_queue_position(
    branch_id: str,
    current_user = Depends(require_roles("CUSTOMER")),
    use_case: AppointmentUseCase = Depends(get_appointment_use_case)
):
    user, _ = current_user
    queue_position = await use_case.get_queue_position(branch_id, str(user.id))
    return queue_position

