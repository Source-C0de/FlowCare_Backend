
from sqlalchemy import Column, JSON, Integer, null, DateTime, String
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from app.infra.db.base import Base





from datetime import datetime, timezone

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    role_type = Column(String, unique=True, nullable=False)
    permissions = Column(JSON, nullable=True, default=list)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )