
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.domain.entities.users import User
from app.domain.repository import user_repo
from app.infra.core.security import hash_password, verify_password
from app.infra.repository.user_repository_impl import UserRepositoryImpl


class RegisterUserUseCase:
    @staticmethod
    async def excute(dto):
        print(dto)
        repo = UserRepositoryImpl()
        existing_user = await repo.find_by_email(dto.email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(dto.password)
        # Create domain entity
        user = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hashed_password,
            phone=dto.phone
        )
      
        # Persist via repository
        await repo.save_user(user)
        return user


class UserLoginUseCase:
    @staticmethod
    async def verify(dto):
        user_repo = UserRepositoryImpl()
        user_info = await user_repo.find_by_email(dto.email)

        if user_info is None:
            raise HTTPException(status_code=400, detail="Email not found")

        user_verified = verify_password(dto.password, user_info.hashed_password)
        print(user_verified)
        if user_verified != True:
            raise HTTPException(status_code=400, detail="Email & Password Not Match")
        return user_info