"""Single declarative Base for all ORM models."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Project-wide base model with automatic timestamps."""

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

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
