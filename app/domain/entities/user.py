"""Pure domain entity — no framework imports."""

from __future__ import annotations

from app.common import Optional, dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    phone: Optional[str] = None
    role_type: Optional[str] = None

    def change_password(self, new_hashed_password: str) -> None:
        self.hashed_password = new_hashed_password


@dataclass
class CustomerProfile:
    id: int
    user_id: UUID
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_image_path: Optional[str] = None
