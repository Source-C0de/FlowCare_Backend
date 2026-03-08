from abc import ABC, abstractmethod

from app.domain.entities.users import CustomerProfiles, User


class UserRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        ...
    @abstractmethod
    async def save_customer_profile(self, customers: CustomerProfiles) -> CustomerProfiles | None:
        ...
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def  get_email_with_role(self, email: str) -> User | None:
        ...

