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

@dataclass
class UpdateBranch:
    name: Optional[str]
    city: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    timezone: Optional[str]
    is_active: Optional[bool]