
from sqlalchemy import Boolean, Column, ForeignKey, String, func, Integer
from sqlalchemy.orm import relationship


from app.infra.db.base import Base
from app.infra.models.roles import Role # ensure roles table is registered


class User(Base):
    __tablename__ = "users"
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=False)
    phone = Column(String(30), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, nullable=False)

    customer_profiles = relationship(
        "CustomerProfile",
        back_populates="users",
        uselist=False,
        cascade="all, delete-orphan"
    )