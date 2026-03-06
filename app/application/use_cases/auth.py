
from uuid import uuid4

from fastapi import HTTPException

from app.domain.entities.users import User
from app.infra.core.security import hash_password
from app.infra.repository.user_repository_impl import UserRepositoryImpl


class RegisterUserUserCase:
    @staticmethod
    async def excute(dto):
        user_repo = UserRepositoryImpl()
        existing_user = await user_repo.find_by_email(dto.email)

        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(dto.password)

        # Create domain entity
        user = User(
            id=uuid4(),
            name=dto.name,
            email=dto.email,
            hashed_password=hashed_password,
            phone=dto.phone,
        )

        # Persist via repository
        await user_repo.save_user(user)

        return user