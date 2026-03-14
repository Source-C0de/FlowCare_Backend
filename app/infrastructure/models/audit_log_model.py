"""AuditLog ORM model."""

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.infrastructure.database.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    uid = Column(UUID(as_uuid=True), unique=True, primary_key=True)
    id = Column(String(100), unique=True, nullable=False)
    action_type = Column(String(50), nullable=False)
    actor_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    log_metadata = Column("metadata", JSONB, nullable=True)

    @hybrid_property
    def formatted_id(self) -> str:
        return f"aud_{self.id}"
