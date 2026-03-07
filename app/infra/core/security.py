"""
Security/auth placeholder.

In production you can add JWT/OAuth2, RBAC, API keys, etc.
"""

from __future__ import annotations

import hashlib
import hmac
import uuid
import base64
import pwd
from fastapi import security
# from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt

from app.config import get_settings


settings = get_settings()

# Argon2id hasher(Singleton)

_ph = PasswordHasher(
    time_cost=settings.ARGON2_TIME_COST,
    memory_cost=settings.ARGON2_MEMORY_COST,
    parallelism=settings.ARGON2_PARALLELISM,
    hash_len=32,
    salt_len=16
)


# use pbkdf2_sha256 to avoid bcrypt 72-byte password backend limits
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# security = security.HTTPBasic()


def hash_password(password: str) -> str:
    # return pwd_context.hash(password)
    return _ph.hash(password)

def verify_password(plain: str, hashed: str)-> bool:
    # return pwd_context.verify(plain, hashed)
    try:
        return _ph.verify(hashed,plain)
    except(VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def password_needs_rehash(hashed: str) -> bool:
    """True when stored hash was produced with older Argon2 parameters."""
    return _ph.check_needs_rehash(hashed)




# JWT
_SECRET = settings.JWT_SECRET_KEY
_ALG = settings.JWT_ALGORITHM


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def create_access_token(
    subject: str,
    role: str,
    extra_claims: dict[str, Any] | None = None
) -> str:

    now = utcnow()
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minitues=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4())

    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, _SECRET, algorithm=_ALG)


def create_refresh_token(
    subject: str,
    family_id: str | None = None
) -> tuple[str, str]:
    
    now = utcnow()
    fid = family_id or str(uuid.uuid4())
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "family": fid,
        "iat": now,
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encond(payload, _SECRET, algorithm=_ALG),  fid


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, _SECRET, algorithm=_ALG)
