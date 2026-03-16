"""Appointment ORM model."""

from app.common import *
from sqlalchemy import Enum
from app.infrastructure.database.base import Base
from app.domain.entities.appointment import AppointmentStatus
class Appointment(Base):
    __tablename__ = "appoinments"

    id = Column(SQL_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    appoinment_no = Column(String(100), unique=True, nullable=False)
    customer_id = Column(SQL_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    service_type_id = Column(String(100), ForeignKey("service_types.id"),nullable=True)
    slot_id = Column(String(100), ForeignKey("slots.id"),nullable=True)
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"),nullable=True)
    status = Column(
        Enum(AppointmentStatus, name="appointment_status"), 
        default=AppointmentStatus.BOOKED,
        nullable=False
    )
    attachment_path = Column(String(500), nullable=True)
    @hybrid_property
    def formatted_id(self) -> str:
        return f"appt_{self.id}"