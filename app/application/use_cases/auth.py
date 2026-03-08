
from uuid import UUID, uuid4

from fastapi import HTTPException,status,Request

from app.domain.entities.users import User
from app.domain.repository import user_repo
from app.infra.core.security import hash_password, verify_password
from app.infra.repository.user_repository_impl import UserRepositoryImpl
from app.infra.core.security import (
    create_access_token,
    create_refresh_token,
    hash_token,
    hash_password
)
from app.api.v1.schemas.user_schema import (
    UserLoginRequest
)
from app.api.v1.schemas.auth import (
    TokenResponse
)
from typing import Tuple

from app.config import settings


_AUTH_ERROR = "Invalid credentials"

class AuthError(Exception):
    """Raised for any authentication failure (opaque to callers)."""
    def __init__(self, message: str = _AUTH_ERROR, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class TokenError(Exception):
    """Raised when a token cannot be decoded or has been revoked."""
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(message)

def build_token_response(
    access_token: str,
    user: User
) -> TokenResponse:
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        user={
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "role": str(user.role_type),
            "status": "active" if user.is_active else "inactive"
        }
    )

class RegisterUserUseCase:
    @staticmethod
    async def excute(dto):
        print(dto)
        repo = UserRepositoryImpl()
        existing_user = await repo.find_by_email(dto.email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(dto.password)
        # Create domain entity
        user = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hashed_password,
            phone=dto.phone
        )
      
        # Persist via repository
        await repo.save_user(user)
        return user


class UserLoginUseCase:
    async def login(
        payload: UserLoginRequest,
        request: Request
    ) -> Tuple[TokenResponse, str, str]:

        user_repo = UserRepositoryImpl()
        user = await user_repo.get_email_with_role(payload.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User Not Found",
                headers={"WWW-Authenticate": "Basic"},
            )
        user_verified = verify_password(payload.password, user.hashed_password)

        access_token = create_access_token(
            subject=str(user.id),
            role=user.role_type,
            extra_claims=None

        )
        refresh_token, family_id = create_refresh_token(subject=str(user.id))
        if not user_verified:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        return build_token_response(access_token, user), refresh_token, family_id



    async def logout(
            refresh_token: str,
    ) -> None:
        token_hash = hash_token(refresh_token)
        # await revoke_token(token_hash)
