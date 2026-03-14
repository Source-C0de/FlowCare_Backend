"""StaffProfile ORM model."""
from app.common import *
from app.infrastructure.database.base import Base



class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(SQL_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey("roles.id"), nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    is_active = Column(Boolean, nullable=False)
