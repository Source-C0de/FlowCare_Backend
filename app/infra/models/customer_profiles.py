from uuid import UUID
from sqlalchemy import Column, ForeignKey, String, Integer



from app.infra.db.base import Base
from sqlalchemy.orm import relationship


class CustomerProfile(Base):
    __table__ = "customer_profiles"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, ForeignKey("users.id"), unique=True, index=True)
    user_name = Column(String, unique=True, nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    id_image_path = Column(String(500), nullable=True)

    user = relationship("User", back_populates="customer_profiles")