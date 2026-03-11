from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class Branch:
    id: str
    name: str
    city: str
    address: str
    phone: Optional[str]
    timezone: str
    is_active: bool