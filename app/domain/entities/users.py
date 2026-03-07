from cgitb import text
from optparse import Option
from typing import Optional
from uuid import UUID


class User:
    def __init__(
        self,
        id: UUID,
        email: str,
        hashed_password: str,
        phone: Optional[str] = None,
        role_type: Optional[str] = None,
        is_active: bool = True,
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.phone = phone
        self.role_type = role_type
        self.is_active = is_active

    def changed_password(self, new_hashed_password: str) -> None:
        self.hashed_password = new_hashed_password


class CustomerProfiles:
    def __init__(
        self,
        id: int,
        user_id: UUID,
        user_name: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        id_image_path: Optional[text]
    ):
        self.id = id
        self.user_id = user_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.id_image_path = id_image_path
