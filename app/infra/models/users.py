
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String, func, Integer, UUID, Text, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET, UUID
from app.infra.db.base import Base
from app.infra.models.roles import Role # ensure roles table is registered


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
        cascade="all, delete-orphan"
    )
    # refresh_tokens = relationship(
    #     "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    # )


# class RefreshToken(Base):
#     __tablename__ = "refresh_tokens"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),nullable=False, index=True)
#     token_hash    = Column(Text, nullable=False, unique=True)   # SHA-256 hex
#     family_id     = Column(UUID(as_uuid=True), nullable=False, index=True)
#     issued_at     = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     expires_at    = Column(DateTime(timezone=True), nullable=False)
#     revoked_at    = Column(DateTime(timezone=True), nullable=True)
#     revoke_reason = Column(String(80), nullable=True)
#     user_agent    = Column(Text, nullable=True)
#     ip_address    = Column(INET, nullable=True)

#     user = relationship("User", back_populates="refresh_tokens")

#     @property
#     def is_valid(self) -> bool:
#         from datetime import timezone
#         return (
#             self.revoked_at is None
#             and self.expires_at > datetime.now(tz=timezone.utc)
#         )