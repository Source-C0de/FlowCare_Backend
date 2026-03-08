import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.infra.db.base import Base


    #   "id": "slot_mus_001",
    #   "branch_id": "br_muscat_001",
    #   "service_type_id": "svc_mus_001",
    #   "staff_id": "usr_staff_001",
    #   "start_at": "2026-02-16T09:00:00+04:00",
    #   "end_at": "2026-02-16T09:15:00+04:00",
    #   "capacity": 1,
    #   "is_active": true


class Slot(Base):
    __tablename__ = "slots"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    service_type_id = Column(String(100), ForeignKey("service_types.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)