import uuid
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.infra.db.base import Base
# "id": "aud_002",
# "actor_id": "usr_cust_001",
# "actor_role": "CUSTOMER",
# "action_type": "APPOINTMENT_BOOKED",
# "entity_type": "APPOINTMENT",
# "entity_id": "appt_001",
# "timestamp": "2026-02-15T10:12:00+04:00",
# "metadata": {
# "slot_id": "slot_mus_001",
# "branch_id": "br_muscat_001",
# "service_type_id": "svc_mus_001"
# }


class AuditLogs(Base):
    __tablename__ = "audit_logs"

    uid = Column(UUID(as_uuid=True), unique=True , primary_key=True)
    id = Column(String(100), unique = True, nullable = False)
    action_type = Column(String(50), nullable=False) # "APPOINTMENT_BOOKED",
    actor_id = Column(UUID(as_uuid=True), nullable=False, index=True) # users_id 
    actor_role = Column(String(50), nullable=False)  # e.g., CUSTOMER
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True) # each entity id
    entity_type = Column(String(50), nullable=False) # e.g., APPOINTMENT
    
    log_metadata = Column("metadata", JSONB, nullable=True)

    @hybrid_property
    def formatted_id(self) -> str:
        return f"aud_{self.id}"
    