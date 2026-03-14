"""Auth-related DTOs — pure data carriers between layers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CustomerRegisterDTO:
    email: str
    password: str
    phone: Optional[str] = None


@dataclass(frozen=True)
class UserLoginDTO:
    email: str
    password: str
