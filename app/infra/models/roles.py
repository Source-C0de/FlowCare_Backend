
from sqlalchemy import Column, JSON, Integer, null
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from app.infra.db.base import Base


class RoleType(str, Enum):
    admin = "ADMIN"
    branch_manager = "BRANCH_MANAGER"
    staff = "STAFF"
    customer = "CUSTOMER"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(SqlEnum(RoleType, name="role_type"), unique=True, nullable=False)
    permissions = Column(JSON, nullable=True, default=list)
