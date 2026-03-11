"""Password hashing — Argon2id (SRP: only hashing concerns)."""

from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from app.config import settings

_ph = PasswordHasher(
    time_cost=settings.ARGON2_TIME_COST,
    memory_cost=settings.ARGON2_MEMORY_COST,
    parallelism=settings.ARGON2_PARALLELISM,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, plain)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def password_needs_rehash(hashed: str) -> bool:
    """True when stored hash was produced with older Argon2 parameters."""
    return _ph.check_needs_rehash(hashed)
