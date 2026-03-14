from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class ServiceTypeDTO:
    name: Optional[str] | None
    branch_id: Optional[str] | None
    description: Optional[str] | None
    duration_minutes: Optional[int] | None
    is_active: Optional[bool] | None

@dataclass
class ServiceTypeUpdateDTO:
    id: Optional[str] | None
    name: Optional[str] | None
    branch_id: Optional[str] | None
    description: Optional[str] | None
    duration_minutes: Optional[int] | None
    is_active: Optional[bool] | None