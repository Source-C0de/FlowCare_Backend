
from sqlalchemy import Boolean, Column, ForeignKey, String, func, Integer
from sqlalchemy.orm import relationship


from app.infra.db.base import Base
from app.infra.models.role import Role  # ensure roles table is registered


class User(Base):
    __tablename__ = "users"
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=False)
    phone = Column(String(30), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    id_image_path = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


