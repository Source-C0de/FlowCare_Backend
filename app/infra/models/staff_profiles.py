from sqlalchemy import Column , Integer , String , Boolean , ForeignKey
from app.infra.db.base import Base
from uuid import uuid4
from datetime import datetime

    # "id": "usr_mgr_001",
    # "username": "mgr_muscat",
    # "password": "Manager@123",
    # "role": "BRANCH_MANAGER",
    # "full_name": "Aisha Al Balushi",
    # "email": "aisha.b@flowcare.local",
    # "branch_id": "br_muscat_001",
    # "is_active": true

class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    username = Column(String(100),unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey("roles.id"), nullable=False)
    branch_id = Column(String(100), ForeignKey("branches.id"), nullable=False)
    is_active = Column(Boolean, nullable=False)