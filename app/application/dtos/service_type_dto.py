from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ServiceTypeDTO:
    name: str
    branch_id: str
    description: str
    duration_minutes: int
    is_active: bool