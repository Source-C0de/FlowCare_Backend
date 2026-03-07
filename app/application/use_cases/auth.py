
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
        user = await user_repo.find_by_email(dto.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="User Not Found",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        user_verified = verify_password(dto.password, user_info.hashed_password)

        if not user_verified:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        return user