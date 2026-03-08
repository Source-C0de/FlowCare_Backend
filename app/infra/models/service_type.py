import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infra.db.base import Base


    #   "id": "svc_mus_001",
    #   "branch_id": "br_muscat_001",
    #   "name": "Customer Support",
    #   "description": "Account questions, basic requests, ticket follow-ups",
    #   "duration_minutes": 15,
    #   "is_active": true

class ServiceType(Base):
    __tablename__ = "service_types"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False) 