"""Pure domain entity for appointments."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Appointment:
    id: UUID
    branch_id: UUID
    service_type_id: UUID
    staff_id: UUID
    start_time: datetime
    end_time: datetime
    is_active: bool = True