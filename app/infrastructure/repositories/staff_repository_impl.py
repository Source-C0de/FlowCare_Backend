from __future__ import annotations
from typing import List, Optional, Any
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.user_model import User as UserModel
from app.infrastructure.models.staff_profile_model import StaffProfile as StaffProfileModel
from app.infrastructure.models.staff_service_type_model import StaffServiceType as StaffServiceTypeModel
from app.domain.entities.user import User
from app.domain.interfaces.staff_repository import StaffRepository
from app.application.dtos.staff_dto import CreateStaffDTO, StaffUpdateDTO, StaffAssignDTO
from app.api.v1.schemas.common import PaginationRequest
from uuid import uuid4
from app.domain.exceptions import DomainException, ConflictException
from app.config import settings
from app.infrastructure.security.hashing import hash_password

class StaffRepositoryImpl(StaffRepository):
    def _to_entity(self, user_model: UserModel, profile_model: StaffProfileModel) -> User:
        return User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.password_hash,
            phone=user_model.phone,
            role_type=profile_model.role,
            username=profile_model.username,
            full_name=profile_model.full_name,
            branch_id=profile_model.branch_id,
            is_active=profile_model.is_active
        )

    async def find_all(self, pagination: PaginationRequest, branch_id: Optional[str] = None) -> List[User]:
        try:
            async with AsyncSessionLocal() as session:
                query = select(UserModel, StaffProfileModel).join(StaffProfileModel, UserModel.id == StaffProfileModel.user_id)
                
                if branch_id:
                    query = query.where(StaffProfileModel.branch_id == branch_id)
                
                if pagination:
                    query = query.offset(pagination.offset).limit(pagination.limit)
                
                result = await session.execute(query)
                rows = result.all()
                return [self._to_entity(u, p) for u, p in rows]
        except Exception as exc:
            raise DomainException(str(exc))

    async def find_by_id(self, staff_id: int) -> Optional[User]:
        try:
            async with AsyncSessionLocal() as session:
                query = select(UserModel, StaffProfileModel).join(
                    StaffProfileModel, UserModel.id == StaffProfileModel.user_id
                ).where(StaffProfileModel.id == staff_id)
                result = await session.execute(query)
                row = result.first()
                if row:
                    return self._to_entity(row[0], row[1])
                return None
        except Exception as exc:
            raise DomainException(str(exc))

    async def create_staff(self, dto: CreateStaffDTO) -> User:
        try:
            async with AsyncSessionLocal() as session:
                user_model = UserModel(
                    email=dto.email,
                    password_hash=hash_password(dto.password),
                    role_id=dto.role_id,
                    phone=dto.phone,
                    is_verified=True,
                    is_active=True,
                )
                session.add(user_model)
                await session.flush()

                role_type = "STAFF"
                if dto.role_id == settings.BRANCH_MANAGER:
                    role_type = "BRANCH_MANAGER"
                elif dto.role_id == settings.ADMIN:
                    role_type = "ADMIN"

                username = dto.email.split('@')[0]
                
                profile_model = StaffProfileModel(
                    user_id=user_model.id,
                    username=username,
                    full_name=dto.name,
                    branch_id=str(dto.branch_id) if dto.branch_id else None,
                    role=role_type,
                    is_active=True,
                )
                session.add(profile_model)
                await session.commit()
                await session.refresh(user_model)
                await session.refresh(profile_model)
                return self._to_entity(user_model, profile_model)
        except IntegrityError:
            await session.rollback()
            raise ConflictException("Staff with this email already exists")
        except Exception as exc:
            await session.rollback()
            raise DomainException(str(exc))

    async def update_staff(self, staff_profile_id: int, dto: StaffUpdateDTO) -> User:
        try:
            async with AsyncSessionLocal() as session:
                query = select(UserModel, StaffProfileModel).join(
                    StaffProfileModel, UserModel.id == StaffProfileModel.user_id
                ).where(StaffProfileModel.id == staff_profile_id)
                result = await session.execute(query)
                row = result.first()
                if not row:
                    raise DomainException("Staff not found")
                
                user_model, profile_model = row
                
                if dto.name:
                    profile_model.full_name = dto.name
                if dto.branch_id:
                    profile_model.branch_id = str(dto.branch_id)
                if dto.phone:
                    user_model.phone = dto.phone
                if dto.is_active is not None:
                    profile_model.is_active = dto.is_active
                    user_model.is_active = dto.is_active
                
                await session.commit()
                await session.refresh(user_model)
                await session.refresh(profile_model)
                return self._to_entity(user_model, profile_model)
        except Exception as exc:
            await session.rollback()
            raise DomainException(str(exc))

    async def delete_staff(self, staff_profile_id: int) -> bool:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(StaffProfileModel).where(StaffProfileModel.id == staff_profile_id)
                )
                profile = result.scalar_one_or_none()
                if not profile:
                    return False
                
                user_id = profile.user_id
                
                await session.execute(delete(StaffProfileModel).where(StaffProfileModel.id == staff_profile_id))
                await session.execute(delete(UserModel).where(UserModel.id == user_id))
                await session.commit()
                return True
        except Exception as exc:
            await session.rollback()
            raise DomainException(str(exc))

    async def assign_service(self, dto: StaffAssignDTO) -> StaffServiceTypeModel:
        try:
            async with AsyncSessionLocal() as session:
                exist_query = select(StaffServiceTypeModel).where(
                    StaffServiceTypeModel.staff_id == dto.staff_id,
                    StaffServiceTypeModel.service_type_id == str(dto.service_type_id)
                )
                exist_res = await session.execute(exist_query)
                if exist_res.scalar_one_or_none():
                    raise DomainException("Staff already assigned to this service type")
                
                assignment = StaffServiceTypeModel(
                    staff_id=dto.staff_id,
                    service_type_id=str(dto.service_type_id),
                    is_active=True
                )
                session.add(assignment)
                await session.commit()
                await session.refresh(assignment)
                return assignment
        except Exception as exc:
            await session.rollback()
            raise DomainException(str(exc))

    async def unassign_service(self, dto: StaffAssignDTO) -> Any:
        try:
            async with AsyncSessionLocal() as session:
                query = select(StaffServiceTypeModel).where(
                    StaffServiceTypeModel.staff_id == dto.staff_id,
                    StaffServiceTypeModel.service_type_id == str(dto.service_type_id)
                )
                res = await session.execute(query)
                assignment = res.scalar_one_or_none()
                
                if not assignment:
                    raise DomainException("Service assignment not found")

                result_data = {
                    "uid": assignment.uid,
                    "staff_id": assignment.staff_id,
                    "service_type_id": assignment.service_type_id
                }
                
                await session.delete(assignment)
                await session.commit()
                return result_data
        except Exception as exc:
            if isinstance(exc, DomainException):
                raise exc
            raise DomainException(str(exc))
