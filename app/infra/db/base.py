import uuid
from datetime import datetime, timezone
from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            index=True,
            nullable=False,
        )

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
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }