from sre_parse import SUCCESS
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBasicCredentials

from app.infra.db.session import get_db
from app.infra.models.users import User
from app.api.v1.schemas.user_schema import (
    CreateUserRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse
)

from app.application.dtos import (
    CustomerRegisterDTO
)

from app.domain.repository.user_repo import UserRepository
from app.application.use_cases import (
    auth
)
# # from app.domain.entities import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201, response_model=UserRegisterResponse)
async def register(request: CreateUserRequest):
    #DTO
    dto = CustomerRegisterDTO(
        email=request.email,
        password=request.password,
        phone=request.phone,
    )
    print(dto)
    user = await auth.RegisterUserUseCase.excute(dto)

    return UserRegisterResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone
    )


@router.post("/login", status_code=201)
async def login(request: UserLoginRequest):
    dto = UserLoginRequest(
        email=request.email,
        password=request.password
    )

    user = await auth.UserLoginUseCase.verify(dto)
    return UserLoginResponse(
        status="success",
        message="successfully login",
        id=str(user.id),
        email=user.email
    )
        

