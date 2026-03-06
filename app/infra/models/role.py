from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from enum import ENUM

class RoleType(str, ENUM):
    admin = "ADMIN",
    manager = "MANAGER",
    staff = "STAFF",
    customer = "CUSTOMER"


class Role(Base):
    __tablename__ = "roles"
    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, default={})

    staff = relationship("Staff", back_populates="role")
