"""Concrete user-repository implementation (DIP: implements the interface)."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.config import settings
from app.domain.entities.user import User, CustomerProfile
from app.domain.exceptions import ConflictException, DomainException
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.customer_profile_model import CustomerProfile as CustomerProfileModel
from app.infrastructure.models.role_model import Role
from app.infrastructure.models.user_model import User as UserModel
from app.infrastructure.models.staff_profile_model import StaffProfile as StaffProfileModel
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from app.infrastructure.models.branch_model import Branch as BranchModel

class UserRepositoryImpl(UserRepository):
    """SQLAlchemy async implementation of UserRepository."""

    async def save_user(self, user: User) -> None:
        try:
            async with AsyncSessionLocal() as session:
                model = UserModel(
                    email=user.email,
                    password_hash=user.hashed_password,
                    role_id=settings.CUSTOMER,
                    phone=user.phone,
                    is_active=True,
                    is_verified=False,
                )
                profile = CustomerProfileModel(
                    customer_email=user.email,
                    id_image_path=user.id_image_path
                )
                session.add(model)
                session.add(profile)
                await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ConflictException("User with this email already exists")
        except Exception as exc:
            await session.rollback()
            raise DomainException(str(exc))

    async def save_customer_profile(self, profile: CustomerProfile) -> Optional[CustomerProfile]:
        # TODO: implement when needed
        return None


    async def save_staff(self, user: User) -> None:
        async with AsyncSessionLocal() as session:
            try:
                model = UserModel(
                    email=user.email,
                    password_hash=user.hashed_password,
                    role_id=settings.STAFF if user.role_type=="STAFF" else settings.BRANCH_MANAGER,
                    phone=user.phone,
                    is_verified=True,
                    is_active=True,
                )
                session.add(model)
                await session.flush()

                profile = StaffProfileModel(
                    user_id=model.id,
                    username=user.username,
                    full_name=user.full_name,
                    branch_id=user.branch_id,
                    role=user.role_type,
                    is_active=True,
                )
                session.add(profile)
                await session.commit()
                await session.refresh(model)
                await session.refresh(profile)
            except IntegrityError:
                await session.rollback()
                raise ConflictException("Staff with this email or username already exists")
            except Exception as exc:
                await session.rollback()
                # Log the actual exception 'exc' here for debugging
                raise DomainException(str(exc))

    async def find_by_email(self, email: str) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            row = result.scalars().first()
            if row is None:
                return None

            return User(
                id=row.id,
                email=row.email,
                hashed_password=row.password_hash,
                phone=row.phone,
            )

    async def get_email_with_role(self, email: str) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserModel, Role.role_type)
                .outerjoin(Role, UserModel.role_id == Role.id)
                .where(UserModel.email == email)
            )
            row = result.first()
            if row is None:
                return None

            user_model = row[0]
            role_type = row[1]

            return User(
                id=user_model.id,
                email=user_model.email,
                hashed_password=user_model.password_hash,
                phone=user_model.phone,
                role_type=role_type,
                is_active=user_model.is_active,
            )
    async def find_by_username(self, username: str) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(StaffProfileModel).where(StaffProfileModel.username == username)
            )
            row = result.scalars().first()
            if row is None:
                return False
            return True

    async def find_by_branch_id(self, branch_id: str) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(BranchModel).where(BranchModel.id == branch_id)
            )
            row = result.scalars().first()
            if row is None:
                return False
            return True