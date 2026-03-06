from typing import Optional
from uuid import UUID


class User:
    def __init__(
        self,
        id: UUID,
        name: str,
        email: str,
        hashed_password: str,
        phone: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.phone = phone

    def changed_password(self, new_hashed_password: str) -> None:
        self.hashed_password = new_hashed_password