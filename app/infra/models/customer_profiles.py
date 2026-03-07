from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID  # <-- use this for PostgreSQL
from app.infra.db.base import Base
from sqlalchemy import Index
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

class CustomerProfile(Base):
    __tablename__ = "customer_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_email = Column(String, ForeignKey("users.email"), unique=True, nullable=False, index=True)
    user_name = Column(String, unique=True, nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    id_image_path = Column(String(500), nullable=True)

    user = relationship("User", back_populates="customer_profiles")