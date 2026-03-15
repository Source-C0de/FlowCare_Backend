"""User repository interface — the port in hexagonal terms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User, CustomerProfile


class UserRepository(ABC):
    """Defines the contract that any user persistence adapter must fulfil."""

    @abstractmethod
    async def save_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def save_staff(self, user: User) -> None:
        ...

    @abstractmethod
    async def save_customer_profile(self, profile: CustomerProfile) -> Optional[CustomerProfile]:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get_email_with_role(self, email: str) -> Optional[User]:
        ...
    @abstractmethod
    async def find_by_username(self, username: str) -> bool:
        ...

    @abstractmethod
    async def find_by_branch_id(self, branch_id: str) -> bool:
        ...
    