from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class SlotDTO:
    branch_id: str
    service_type_id: str
    staff_id: Optional[str] | None
    start_time: Optional[datetime]| None
    end_time: Optional[datetime]| None
    is_booked: Optional[bool] | None
    # capacity: Optional[int] | None
    is_active: Optional[bool] | None

@dataclass
class SlotUpdateDTO:
    id: Optional[str] | None
    branch_id: Optional[str] | None
    service_type_id: Optional[str] | None
    staff_id: Optional[str] | None
    start_time: Optional[datetime] | None
    end_time: Optional[datetime] | None
    # capacity: Optional[int] | None
    is_active: Optional[bool] | None
    is_booked: Optional[bool] | None



__all__ = [
    "SlotDTO",
    "SlotUpdateDTO",
]
