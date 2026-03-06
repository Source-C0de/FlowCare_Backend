
from fastapi import HTTPException
from sqlalchemy import select

from app.domain.entities.users import User
from app.domain.repository.user_repo import UserRepository
from app.infra.db.session import AsyncSessionLocal
from app.infra.models.users import User as UserModel
from sqlalchemy.exc import IntegrityError
from app.config import Settings


class UserRepositoryImpl(UserRepository):
    async def save_user(self, user: User) -> None:
        try:
            async with AsyncSessionLocal() as session:
                model = UserModel(
                    name=user.name,
                    email=user.email,
                    password_hash=user.hashed_password,
                    role_id=3,
                    phone=user.phone,
                )
                session.add(model)
                await session.commit()
        except IntegrityError:
            print("Test")
            await session.rollback()
        except Exception as e:
            await session.rollback()
            print("Check")
            raise HTTPException(e)

    async def find_by_email(self, email: str) -> User | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            row = result.scalars().first()

            if row is None:
                return None

            return User(
                id=row.id,
                email=row.email,
                name=row.name,
                hashed_password=row.password_hash,
            )



