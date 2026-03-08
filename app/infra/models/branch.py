import uuid
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.infra.db.base import Base

#       "id": "br_muscat_001",
#       "name": "FlowCare Muscat - Al Khuwair",
#       "city": "Muscat",
#       "address": "Al Khuwair, Muscat",
#       "timezone": "Asia/Muscat",
#       "is_active": true


class Branch(Base):
    __tablename__ = "branches"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(500), nullable=False)
    timezone = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)



