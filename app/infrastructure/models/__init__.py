"""ORM model registry — import all models here so Alembic discovers them."""

from app.infrastructure.models.role_model import Role
from app.infrastructure.models.user_model import User
from app.infrastructure.models.customer_profile_model import CustomerProfile
from app.infrastructure.models.appointment_model import Appointment
from app.infrastructure.models.branch_model import Branch
from app.infrastructure.models.slot_model import Slot
from app.infrastructure.models.service_type_model import ServiceType
from app.infrastructure.models.staff_service_type_model import StaffServiceType
from app.infrastructure.models.staff_profile_model import StaffProfile
from app.infrastructure.models.audit_log_model import AuditLog

__all__ = [
    "Role",
    "User",
    "CustomerProfile",
    "Appointment",
    "Branch",
    "Slot",
    "ServiceType",
    "StaffServiceType",
    "StaffProfile",
    "AuditLog",
]
