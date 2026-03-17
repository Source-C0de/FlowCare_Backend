"""API-layer Dependency Injection container.

This is where we wire interfaces to implementations (DIP).
FastAPI's Depends() system injects these into endpoints.
"""

from __future__ import annotations

from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.domain.interfaces.branch_repository import BranchRepository
from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.domain.interfaces.slot_repository import SlotRepository
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.domain.interfaces.file_repository import FileRepository
from app.domain.interfaces.staff_repository import StaffRepository


from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.branch_repository_impl import BranchRepositoryImpl
from app.infrastructure.repositories.service_type_repository_impl import ServiceTypeRepositoryImpl
from app.infrastructure.repositories.slot_repository_impl import SlotRepositoryImpl
from app.infrastructure.repositories.audit_logs_repository_impl import AuditLogsRepositoryImpl
from app.infrastructure.repositories.file_repository_impl import FileRepositoryImpl
from app.infrastructure.repositories.staff_repository_impl import StaffRepositoryImpl

from app.application.use_cases.auth import AuthUseCase
from app.application.use_cases.appointment import AppointmentUseCase
from app.application.use_cases.branch import BranchUseCase
from app.application.use_cases.service_type import ServiceTypeUseCase
from app.application.use_cases.slots import SlotUseCase
from app.application.use_cases.audit_logs import AuditLogsUseCase
from app.application.use_cases.staff import StaffUseCase


# ── Repository factories ──────────────────────────────────────


def get_user_repository() -> UserRepository:
    return UserRepositoryImpl()

def get_appointment_repository() -> AppointmentRepository:
    return AppointmentRepositoryImpl()

def get_branch_repository() -> BranchRepository:
    return BranchRepositoryImpl()

def get_service_type_repository() -> ServiceTypeRepository:
    return ServiceTypeRepositoryImpl()

def get_slot_repository() -> SlotRepository:
    return SlotRepositoryImpl()

def get_audit_logs_repository() -> AuditLogsRepository:
    return AuditLogsRepositoryImpl()

def get_file_repository() -> FileRepository:
    return FileRepositoryImpl()

def get_staff_repository() -> StaffRepository:
    return StaffRepositoryImpl()

# ── Use-case factories ────────────────────────────────────────

def get_auth_use_case() -> AuthUseCase:
    return AuthUseCase(user_repo = get_user_repository(), file_repo=get_file_repository())


def get_appointment_use_case() -> AppointmentUseCase:
    return AppointmentUseCase(
        appointment_repo=get_appointment_repository(),
        file_repo=get_file_repository(),
        audit_repo=get_audit_logs_repository()
    )

def get_branch_use_case() -> BranchUseCase:
    return BranchUseCase(branch_repository=get_branch_repository())


def get_service_type_use_case() -> ServiceTypeUseCase:
    return ServiceTypeUseCase(service_type_repository=get_service_type_repository())


def get_slot_use_case() -> SlotUseCase:
    return SlotUseCase(slot_repository=get_slot_repository())


def get_audit_use_case() -> AuditLogsUseCase:
    return AuditLogsUseCase(audit_logs_repo=get_audit_logs_repository())


def get_staff_use_case() -> StaffUseCase:
    return StaffUseCase(
        user_repo=get_user_repository(),
        staff_repo=get_staff_repository(),
        file_repo=get_file_repository(),
        audit_repo=get_audit_logs_repository()
    )





