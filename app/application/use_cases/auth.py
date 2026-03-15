from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.domain.entities.user import User

from app.application.dtos import *
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
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
from app.domain.interfaces import FileRepository

class AuthUseCase:
    def __init__(self, user_repo: UserRepository, file_repo: FileRepository)-> None:
        self._repo = user_repo
        self._file_repo = file_repo

    async def register_customer(self, dto: UserRegisterDTO) -> User:
        _check_user = await self._repo.find_by_email(dto.email)
        if _check_user is not None:
            raise ConflictException("Email already registered") 
        
        hashed = hash_password(dto.password)
        # For now, default role logic can be here or handled by the repository
        # If it's RegisterUserDTO, maybe it's always 'CUSTOMER'
        # If it's StaffRegisterDTO, it has a 'role'
        
        role_type = getattr(dto, 'role', 'CUSTOMER')
        # if role_type == "CUSTOMER":
            
        # else:
        #     id_image_path = None
        
        await validate_file(dto.id_image, IMAGE_TYPE, settings.CUSTOMER_ID_MAX_SIZE)
        id_image_path = await self._file_repo.upload_file(dto.id_image, "id_images")
        
        user_entity = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hashed, # Repo seems to use password_hash or hashed_password? I should check.
            phone=dto.phone,
            role_type=role_type,
            id_image_path=id_image_path
        )
        await self._repo.save_user(user_entity) 
        # if role_type ==  "CUSTOMER":
        #     await self._repo.save_user(user_entity)
        # else:
        #     await self._repo.save_staff(user_entity)
        return user_entity


    async def register_staff(self, dto: StaffRegisterDTO) -> User:
        _check_user = await self._repo.find_by_email(dto.email)
        if _check_user is not None:
            print(_check_user)
            raise ConflictException("Email already registered") 
        _check_staff = await self._repo.find_by_username(dto.username)
        if _check_staff is True:
            raise ConflictException("Username already registered")
        _check_branch = await self._repo.find_by_branch_id(dto.branch_id)
        if _check_branch is False:
            raise ConflictException("Branch not found")
        
        hashed = hash_password(dto.password)

        user_entity = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hashed,
            username=dto.username,
            full_name=dto.full_name,
            phone=dto.phone,
            branch_id=dto.branch_id,
            role_type=dto.role,
        )
        await self._repo.save_staff(user_entity)
        return user_entity

    async def login(self, user: UserLoginDTO)-> Tuple[User, str, str, str]:
        
        _user = await self._repo.get_email_with_role(user.email)
        if _user is None:
            raise UserNotFoundException("User not found")
        
        if not verify_password(user.password, _user.hashed_password):
            raise UnauthorizedException("Invalid credentials")
        
        if not _user.is_active:
            raise ForbiddenException("Account is inactive")
        
        access_token = create_access_token(
            subject=str(_user.id),
            role=_user.role_type or "",
        )       
        refresh_token, family_id = create_refresh_token(subject=str(_user.id))

        return _user,access_token,refresh_token,family_id

    async def logout(self,refresh_token: str | None):
        if refresh_token is None:
            return
        _token_hash = hash_token(refresh_token)
        # TODO: persist revocation to a token blacklist table
        pass




__all__ = [
    "AuthUseCase"
]
