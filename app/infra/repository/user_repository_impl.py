
from fastapi import HTTPException
from sqlalchemy import select

from app.domain.entities.users import User, CustomerProfiles
from app.domain.repository.user_repo import UserRepository
from app.infra.db.session import AsyncSessionLocal
from app.infra.models.customer_profiles import CustomerProfile
from app.infra.models.users import User as UserModel
from app.infra.models.customer_profiles import CustomerProfile as CustomerProfileModel
from sqlalchemy.exc import IntegrityError
from app.config import settings


class UserRepositoryImpl(UserRepository):
    async def save_user(self, user: User) -> None:
        try:
            async with AsyncSessionLocal() as session:
                model = UserModel(
                    email=user.email,
                    password_hash=user.hashed_password,
                    role_id=settings.CUSTOMER,
                    phone=user.phone,
                )
                model_customer = CustomerProfileModel(
                    customer_email=user.email
                )
                session.add(model)
                session.add(model_customer)
                await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(IntegrityError)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def save_customer_profile(self, user: User) -> None:
        try:
            async with AsyncSessionLocal() as session:
                print(user.id)

                # model = CustomerProfileModel(
                #     user_id=user.id
                # )
                # session.add(model)
                # await session.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



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
                hashed_password=row.password_hash,
                phone=row.phone,
            )



