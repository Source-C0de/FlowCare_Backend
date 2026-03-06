from enum import Enum

from sqlalchemy import Column, JSON, String

from app.infra.db.base import Base

class RoleType(str, Enum):
    admin = "ADMIN"
    manager = "MANAGER"
    staff = "STAFF"
    customer = "CUSTOMER"


class Role(Base):
    __tablename__ = "roles"
    name = Column(String(50), unique=True, nullable=False)
    permissions = Column(JSON, default=dict)
