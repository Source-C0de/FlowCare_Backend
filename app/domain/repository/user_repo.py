from abc import ABC, abstractmethod
from app.domain.entities.users import User


class UserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User):
        pass

    def find_by_email(self, email: str) -> User | None:
        pass