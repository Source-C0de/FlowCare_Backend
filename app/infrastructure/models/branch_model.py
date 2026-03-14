"""Branch ORM model."""

from app.common import *
from app.infrastructure.database.base import Base


class Branch(Base):
    __tablename__ = "branches"

    uid = Column(SQL_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(500), nullable=False)
    phone = Column(String(30), nullable=True)
    timezone = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)
