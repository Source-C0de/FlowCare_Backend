"""User ORM model."""

import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base
from app.infrastructure.models.role_model import Role  # noqa: F401 — register dependency


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=False)
    phone = Column(String(30), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, nullable=False)

    customer_profiles = relationship(
        "CustomerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
