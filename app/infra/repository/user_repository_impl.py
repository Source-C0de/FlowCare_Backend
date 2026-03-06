
from app.domain.entities.users import User
from app.domain.repository.user_repo import UserRepository
from app.infra.models.users import User as UserModel
from app.infra.db.database import SessionLocal


class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self.db = SessionLocal()

    def save_user(self, user: User):
        model = UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.hashed_password,
            phone=user.phone
        )
        self.db.add(model)
        self.db.commit()

    def find_by_email(self, email: str) -> User | None:
        result = self.db.query(UserModel).filter_by(email=email).first()

        if not result:
            return None

        return User(
            id=result.id,
            email=result.email,
            name=result.name,
            hashed_password=result.hashed_password
        )
