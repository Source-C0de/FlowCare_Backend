"""Auth-related DTOs — pure data carriers between layers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from fastapi import UploadFile


@dataclass(frozen=True)
class UserRegisterDTO:
    email: str
    password: str
    id_image: UploadFile
    phone: Optional[str] = None


@dataclass(frozen=True)
class UserLoginDTO:
    email: str
    password: str


@dataclass(frozen=True)
class StaffRegisterDTO:
    email: str
    password: str
    role: str
    phone: Optional[str] = None



__all__ = [
    "UserRegisterDTO",
    "UserLoginDTO",
    "StaffRegisterDTO",
]
