"""Abstract repository interfaces (ports).

The domain defines WHAT it needs; infrastructure provides HOW.
"""

from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.domain.interfaces.file_repository import FileRepository

__all__ = ["UserRepository", "AppointmentRepository", "BranchRepository", "FileRepository"]
