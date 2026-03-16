import enum
from app.common import datetime, Optional, dataclass
from uuid import UUID

class AppointmentStatus(enum.Enum):
    BOOKED = "BOOKED"
    CHECKED_IN = "CHECKED_IN"
    NO_SHOW = "NO_SHOW"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

@dataclass
class Appointment:
    id: UUID
    appoinment_no: str
    customer_id: UUID
    branch_id: str
    service_type_id: Optional[str] = None
    slot_id: Optional[str] = None
    staff_id: Optional[int] = None
    status: AppointmentStatus = AppointmentStatus.BOOKED
    attachment_path: Optional[str] = None