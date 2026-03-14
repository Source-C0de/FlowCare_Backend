"""Slot ORM model."""

from app.common import *
from app.infrastructure.database.base import Base



class Slot(Base):
    __tablename__ = "slots"

    uid = Column(SQL_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    service_type_id = Column(String(100), ForeignKey("service_types.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
