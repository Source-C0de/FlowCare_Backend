from fastapi import HTTPException, status

from app.domain.repository.appointment import AppointmentRepository
from app.domain.models.appointment import Appointment
from app.infra.database.models.appointment import Appointment as AppointmentModel

class AppointmentRepositoryImpl(AppointmentRepository):
    def __init__(self):
        self.appointments = []

    async def create_appointment(self, appointment: Appointment) -> Appointment:
        try:
            appointment = AppointmentModel(
                branch_id=appointment.branch_id,
                service_type_id=appointment.service_type_id,
                staff_id=appointment.staff_id,
                start_time=appointment.start_time,
                end_time=appointment.end_time,
                capacity=appointment.capacity,
                is_active=appointment.is_active
            )
            return appointment
        except Exception as e:
            raise HTTPException(e)
        self.appointments.append(appointment)
        return appointment

    async def get_appointment(self, appointment_id: str) -> Appointment | None:
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    async def get_appointments(self) -> list[Appointment]:
        return self.appointments
