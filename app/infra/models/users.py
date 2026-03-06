import uuid 
from sqlalchemy import Column, ForeignKey, String, func, Boolean
from sqlalchemy.orm import relationship
from app.infra.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=False)
    phone = Column(String(30), nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    id_image_path = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
