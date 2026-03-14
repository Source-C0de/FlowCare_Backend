"""StaffServiceType ORM model."""

import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.database.base import Base


class StaffServiceType(Base):
    __tablename__ = "staff_service_types"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"), nullable=False)
    service_type_id = Column(String(100), ForeignKey("service_types.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
