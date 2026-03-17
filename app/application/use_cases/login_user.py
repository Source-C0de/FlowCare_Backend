"""Login-user use case."""

from __future__ import annotations

from typing import Tuple

from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedException, ForbiddenException
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.security.hashing import verify_password
from app.infrastructure.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
)


from app.application.dtos.auth_dto import UserLoginDTO

class LoginUserUseCase:
    """Orchestrates user login — verifies credentials, produces tokens."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(self, dto: UserLoginDTO) -> Tuple[User, str, str, str]:
        """
        Returns
        -------
        (user, access_token, refresh_token, family_id)

        Raises
        ------
        UnauthorizedException  – bad credentials or user not found
        ForbiddenException     – account inactive
        """
        user = await self._repo.get_email_with_role(dto.email)

        if user is None:
            raise UnauthorizedException("Invalid credentials")

        if not verify_password(dto.password, user.password_hash):
            raise UnauthorizedException("Invalid credentials")

        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        access_token = create_access_token(
            subject=str(user.id),
            role=user.role_type or "",
        )
        refresh_token, family_id = create_refresh_token(subject=str(user.id))

        return user, access_token, refresh_token, family_id



__all__ = [
    "LoginUserUseCase"
]
