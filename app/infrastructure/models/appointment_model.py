"""Appointment ORM model."""

import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.infrastructure.database.base import Base


class Appointment(Base):
    __tablename__ = "appoinments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    appoinment_no = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    slot_id = Column(String(100), ForeignKey("slots.id"))
    service_type_id = Column(String(100), ForeignKey("service_types.id"))
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"))
    status = Column(String(20), nullable=False)

    @hybrid_property
    def formatted_id(self) -> str:
        return f"appt_{self.id}"
