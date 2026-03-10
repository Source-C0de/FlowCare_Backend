


class AppointmentRepository(ABC):
    @abstractmethod
    async def create_appointment(self, appointment: Appointment) -> Appointment:
        ...
    @abstractmethod
    async def get_appointment(self, appointment_id: str) -> Appointment | None:
        ...
    @abstractmethod
    async def get_appointments(self) -> list[Appointment]:
        ...
        