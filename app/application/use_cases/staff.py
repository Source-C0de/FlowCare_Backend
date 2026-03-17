from __future__ import annotations
from typing import Tuple, TYPE_CHECKING, List, Any
from uuid import uuid4

if TYPE_CHECKING:
    from app.domain.entities.user import User

from app.application.dtos import *
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.domain.interfaces.staff_repository import StaffRepository
from app.domain.interfaces.audit_logs_repository import AuditLogsRepository
from app.domain.exceptions import (
    UserNotFoundException, 
    UnauthorizedException,
    ForbiddenException,
    ConflictException
)
from app.infrastructure.security.hashing import hash_password, verify_password
from app.infrastructure.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
)
from app.infrastructure.security.token_utils import hash_token
from app.infrastructure.utils.file_validation import validate_file, IMAGE_TYPE
from app.config import settings
from app.domain.interfaces.file_repository import FileRepository
from app.domain.entities.audit_logs import AuditLog
from uuid import UUID

class StaffUseCase:
    def __init__(self, user_repo: UserRepository, staff_repo: StaffRepository, file_repo: FileRepository, audit_repo: AuditLogsRepository)-> None:
        self._user_repo = user_repo
        self._repo = staff_repo
        self._file_repo = file_repo
        self._audit_repo = audit_repo

    async def find_all(self, current_user: User, pagination: PaginationDTO) -> list[User]:
        user, role = current_user
        if role != "ADMIN" and pagination.branch_id and pagination.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to find staff in this branch")
        
        if role == "ADMIN":
            return await self._repo.find_all(pagination, pagination.branch_id)
            
        return await self._repo.find_all(pagination, user.branch_id)

    async def find_by_id(self, current_user: User, staff_id: int) -> User:
        user, role = current_user
        staff = await self._repo.find_by_id(staff_id)
        if not staff:
             raise UserNotFoundException("Staff not found")
             
        if role != "ADMIN" and staff.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to find staff in this branch")
        return staff

    async def create_staff(self, current_user: User, dto: CreateStaffDTO) -> User:

        user , role = current_user
        if role != "ADMIN" and dto.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to create staff in this branch")

        result = await self._user_repo.find_by_email(dto.email)
        if result:
            raise ConflictException("Email email already exists")

        staff = await self._repo.create_staff(dto)

        await self._audit_repo.write_audit_log(
            AuditLog(
                action="staff_created",
                actor_id=user.id,
                actor_role=role,
                entity_id=staff.id, 
                entity_type="staff",
                branch_id=str(dto.branch_id) if dto.branch_id else None,
                metadata={
                    "role_id": str(dto.role_id) if dto.role_id else None,
                    "branch_id": str(dto.branch_id) if dto.branch_id else None,
                    "status": "active",
                },
            )
        )
        return staff

    async def update_staff(self, current_user: User, staff_id: int, dto: StaffUpdateDTO) -> User:
        user , role = current_user
        
        staff = await self._repo.find_by_id(staff_id)
        if not staff:
            raise UserNotFoundException("Staff not found")

        if role != "ADMIN" and staff.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to update staff in this branch")   
        
        staff = await self._repo.update_staff(staff_id, dto)

        # await self._audit_repo.write_audit_log(
        #     AuditLog(
        #         action="staff_updated",
        #         actor_id=user.id,
        #         actor_role=role,
        #         entity_id=staff.id, 
        #         entity_type="staff",
        #         branch_id=str(staff.branch_id) if staff.branch_id else None,
        #         metadata={
        #             "role_id": str(staff.role_id) if staff.role_id else None,
        #             "branch_id": str(staff.branch_id) if staff.branch_id else None,
        #             "status": "active",
        #         },
        #     )
        # )
        return staff

    async def delete_staff(self, staff_id: int) -> User:
        return await self._repo.delete_staff(staff_id)

    async def assign_service(self, current_user: User, dto: StaffAssignDTO) -> Any:
        user , role = current_user
        
        staff = await self._repo.find_by_id(dto.staff_id)
        if not staff:
            raise UserNotFoundException("Staff not found")

        if role != "ADMIN" and staff.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to assign service to this staff")
        
        result = await self._repo.assign_service(dto)
        await self._audit_repo.write_audit_log(
            AuditLog(
                action="staff_assigned",
                actor_id=user.id,
                actor_role=role,
                entity_id=result.uid, 
                entity_type="staff_service_type",
                branch_id=str(staff.branch_id) if staff.branch_id else None,
                metadata={
                    "staff_id": str(dto.staff_id) if dto.staff_id else None,
                    "service_type_id": str(dto.service_type_id) if dto.service_type_id else None,
                },
            )
        )
        return result

    async def unassign_service(self, current_user: User, dto: StaffAssignDTO) -> None:
        user, role = current_user
        staff = await self._repo.find_by_id(dto.staff_id)
        if not staff:
            raise UserNotFoundException("Staff not found")

        if role != "ADMIN" and staff.branch_id != user.branch_id:
            raise ForbiddenException("You are not authorized to unassign service from this staff")

        result =  await self._repo.unassign_service(dto)
        await self._audit_repo.write_audit_log(
            AuditLog(
                action="staff_unassigned",
                actor_id=user.id,
                actor_role=role,
                entity_id=result["uid"], 
                entity_type="staff_service_type",
                branch_id=str(staff.branch_id) if staff.branch_id else None,
                metadata={
                    "staff_id": str(dto.staff_id) if dto.staff_id else None,
                    "service_type_id": str(dto.service_type_id) if dto.service_type_id else None,
                },
            )
        )
        return result


__all__ = [
    "StaffUseCase"
]