"""RBAC middleware — token extraction & current user resolution."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.security.jwt_handler import decode_token
from app.infrastructure.database.session import get_db
from app.infrastructure.models.user_model import User
from app.infrastructure.models.role_model import Role

_bearer = HTTPBearer(auto_error=False)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
_FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions",
)


@dataclass(frozen=True)
class TokenClaims:
    sub: str
    role: str
    jti: str
    branch_id: str | None


def _extract_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> TokenClaims:
    if credentials is None:
        raise _CREDENTIALS_EXCEPTION
    try:
        plain_token = decode_token(credentials.credentials)
    except JWTError:
        raise _CREDENTIALS_EXCEPTION

    return TokenClaims(
        sub=plain_token["sub"],
        role=plain_token["role"],
        jti=plain_token.get("jti", ""),
        branch_id=plain_token.get("branch_id"),
    )


async def get_current_user(
    token: TokenClaims = Depends(_extract_token),
    db: AsyncSession = Depends(get_db),
) -> tuple[User, str]:
    result = await db.execute(select(User).where(User.id == token.sub))
    user: User | None = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise _CREDENTIALS_EXCEPTION

    return user, token.role


def require_roles(*allowed_roles: str):
    """Dependency factory that enforces role-based access."""

    async def _check(current: tuple[User, str] = Depends(get_current_user)) -> tuple[User, str]:
        user, role = current
        if role not in allowed_roles:
            raise _FORBIDDEN_EXCEPTION
        return user, role

    return _check