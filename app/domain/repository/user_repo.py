from abc import ABC, abstractmethod

from app.domain.entities.users import User


class UserRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        ...