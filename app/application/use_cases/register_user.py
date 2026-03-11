"""Register-user use case (SRP: one reason to change)."""

from __future__ import annotations

from uuid import uuid4

from app.application.dtos.auth_dto import CustomerRegisterDTO
from app.domain.entities.user import User
from app.domain.exceptions import ConflictException
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.security.hashing import hash_password


class RegisterUserUseCase:
    """Orchestrates customer registration."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(self, dto: CustomerRegisterDTO) -> User:
        existing = await self._repo.find_by_email(dto.email)
        if existing is not None:
            raise ConflictException("Email already registered")

        hashed = hash_password(dto.password)

        user = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hashed,
            phone=dto.phone,
        )

        await self._repo.save_user(user)
        return user
