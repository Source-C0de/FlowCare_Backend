from __future__ import annotations

from dataclasses import dataclass

@dataclass
class CreateBranchDTO:
    name: str
    city: str
    address: str
    phone: str
    timezone: str | None


@dataclass
class UpdateBranchDTO:
    name: Optional[str]
    city: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    timezone: Optional[str]
    is_active: Optional[bool]

__all__ = [
    "CreateBranchDTO",
    "UpdateBranchDTO"
]