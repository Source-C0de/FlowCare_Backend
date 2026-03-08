import uuid
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infra.db.base import Base
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

class Appoinment(Base):
    __tablename__ = "appoinments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    appoinment_no = Column(String(100), unique=True, nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    slot_id = Column(String(100), ForeignKey("slots.id"))
    service_type_id = Column(String(100), ForeignKey("service_types.id"))
    staff_id = Column(Integer, ForeignKey("staff_profiles.id"))
    status = Column(String(20), nullable=False)
    # start_at = Column(DateTime)
    # end_at = Column(DateTime)
    # capacity = Column(Integer)
    # is_active = Column(Boolean)


    # @event.listens_for(Appointment, "before_insert")
    # def generate_appt_id(mapper, connection, target):
    #     result = connection.execute(
    #         select(func.count(Appointment.id))
    #     )
    #     count = result.scalar() or 0
    #     width = max(3, len(str(count + 1)))
    #     target.id = f"appt_{(count + 1):0{width}d}"

    @hybrid_property
    def formatted_id(self) -> str:
        return f"appt_{self.id}"