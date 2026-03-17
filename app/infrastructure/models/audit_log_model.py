"""AuditLog ORM model."""

from app.common import *
from app.infrastructure.database.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    uid = Column(SQL_UUID(as_uuid=True), unique=True, primary_key=True)
    id = Column(String(100), unique=True, nullable=False)
    action_type = Column(String(50), nullable=False)
    actor_id = Column(SQL_UUID(as_uuid=True), nullable=False, index=True)
    actor_role = Column(String(50), nullable=False)
    entity_id = Column(SQL_UUID(as_uuid=True), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    branch_id = Column(String(100),ForeignKey("branches.id"), nullable=True)
    log_metadata = Column("metadata", JSONB, nullable=True)

    @hybrid_property
    def formatted_id(self) -> str:
        return f"aud_{self.id}"
