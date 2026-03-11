"""Abstract repository interfaces (ports).

The domain defines WHAT it needs; infrastructure provides HOW.
"""

from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.appointment_repository import AppointmentRepository

__all__ = ["UserRepository", "AppointmentRepository"]
