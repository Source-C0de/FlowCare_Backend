import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infra.db.base import Base
from datetime import datetime



class StaffServiceType(Base):
    __tablename__ = "staff_service_types"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"), nullable=False)
    service_type_id = Column(String(100), ForeignKey("service_types.id"), nullable=False)
    # assigned_at = Column(datetime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
