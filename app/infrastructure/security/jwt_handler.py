"""JWT creation & decoding (SRP: only JWT concerns)."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.config import settings

_SECRET = settings.JWT_SECRET_KEY
_ALG = settings.JWT_ALGORITHM


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def create_access_token(
    subject: str,
    role: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = _utcnow()
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, _SECRET, algorithm=_ALG)


def create_refresh_token(
    subject: str,
    family_id: str | None = None,
) -> tuple[str, str]:
    now = _utcnow()
    fid = family_id or str(uuid.uuid4())
    payload: dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "family": fid,
        "iat": now,
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALG), fid


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, _SECRET, algorithms=[_ALG])
