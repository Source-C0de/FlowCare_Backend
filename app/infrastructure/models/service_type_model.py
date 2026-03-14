"""ServiceType ORM model."""

from app.common import *
from app.infrastructure.database.base import Base

class ServiceType(Base):
    __tablename__ = "service_types"

    uid = Column(SQL_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
