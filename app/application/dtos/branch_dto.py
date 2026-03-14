from __future__ import annotations

from dataclasses import dataclass

@dataclass
class CreateBranchDTO:
    name: str
    city: str
    address: str
    phone: str
    timezone: str | None
    is_active: bool


__all__ = [
    "CreateBranchDTO",
]