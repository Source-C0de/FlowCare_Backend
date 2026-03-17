from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class ServiceTypeDTO:
    branch_id: str
    name: str
    description: Optional[str] | None
    duration_minutes: int

@dataclass
class ServiceTypeUpdateDTO:
    branch_id: str
    service_type_id: str
    name: Optional[str] | None
    description: Optional[str] | None
    duration_minutes: Optional[int] | None
    is_active: Optional[bool] | None



__all__ = [
    "ServiceTypeDTO",
    "ServiceTypeUpdateDTO",
]
