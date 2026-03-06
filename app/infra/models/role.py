from enum import Enum

from sqlalchemy import Column, JSON, String, Integer, null

from app.infra.db.base import Base

class RoleType(str, Enum):
    admin = "ADMIN"
    manager = "MANAGER"
    staff = "STAFF"
    customer = "CUSTOMER"


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, default=dict)
