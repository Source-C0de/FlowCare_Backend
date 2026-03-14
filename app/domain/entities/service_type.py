from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ServiceType:
    id: str
    name: str
    branch_id: str
    description: str
    duration_minutes: int
    is_active: bool