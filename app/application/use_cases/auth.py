
from uuid import uuid4
from fastapi import HTTPException
from app.domain.repository.user_repo import UserRepository
from app.infra.models.users import User
from app.infra.core.security import hash_password


class RegisterUserUserCase:
    @staticmethod
    def excute(dto):
        existing_user = UserRepository.find_by_email(dto.email)

        if existing_user.scaler_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(dto.password)

        # Create domain entity
        user = User(
            id=uuid4(),
            name=dto.name,
            email=dto.email,

            password_hash=hashed_password,
        )
        # Save using repository
        # user_repository.save(user)

        return user