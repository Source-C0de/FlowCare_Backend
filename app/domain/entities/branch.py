from __future__ import annotations

from app.common import Optional, dataclass

@dataclass
class Branch:
    id: str
    name: str
    city: str
    address: str
    phone: Optional[str]
    timezone: str
    is_active: bool