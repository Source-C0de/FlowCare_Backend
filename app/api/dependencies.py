"""API-layer Dependency Injection container.

This is where we wire interfaces to implementations (DIP).
FastAPI's Depends() system injects these into endpoints.
"""

from __future__ import annotations

from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.appointment_repository import AppointmentRepository
from app.domain.interfaces.branch_repository import BranchRepository
from app.domain.interfaces.service_type_repository import ServiceTypeRepository
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.branch_repository_impl import BranchRepositoryImpl
from app.infrastructure.repositories.service_type_repository_impl import ServiceTypeRepositoryImpl

from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.logout_user import LogoutUserUseCase
from app.application.use_cases.book_appointment import BookAppointmentUseCase
from app.application.use_cases.branch import BranchUseCase
from app.application.use_cases.service_type import ServiceTypeUseCase


# ── Repository factories ──────────────────────────────────────

def get_user_repository() -> UserRepository:
    return UserRepositoryImpl()


def get_appointment_repository() -> AppointmentRepository:
    return AppointmentRepositoryImpl()

def get_branch_repository() -> BranchRepository:
    return BranchRepositoryImpl()

def get_service_type_repository() -> ServiceTypeRepository:
    return ServiceTypeRepositoryImpl()


# ── Use-case factories ────────────────────────────────────────

def get_register_use_case() -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo=get_user_repository())


def get_login_use_case() -> LoginUserUseCase:
    return LoginUserUseCase(user_repo=get_user_repository())


def get_logout_use_case() -> LogoutUserUseCase:
    return LogoutUserUseCase()


def get_book_appointment_use_case() -> BookAppointmentUseCase:
    return BookAppointmentUseCase(appointment_repo=get_appointment_repository())

def get_branch_use_case() -> BranchUseCase:
    return BranchUseCase(branch_repository=get_branch_repository())


def get_service_type_use_case() -> ServiceTypeUseCase:
    return ServiceTypeUseCase(service_type_repository=get_service_type_repository())
