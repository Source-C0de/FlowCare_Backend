from sre_parse import SUCCESS
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form, Request, Response, Cookie
from fastapi.responses import JSONResponse
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
from app.api.v1.schemas.auth import (
    TokenResponse,
    MessageResponse
)

from app.application.dtos import (
    CustomerRegisterDTO
)

from app.domain.repository.user_repo import UserRepository
from app.application.use_cases.auth import (
    RegisterUserUseCase,
    UserLoginUseCase
)
from app.config import settings
# # from app.domain.entities import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


_COOKIE_NAME = settings.REFRESH_COOKIE_NAME

def _set_refresh_token_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=_COOKIE_NAME,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/api/v1/auth",
    )

@router.post("/register", status_code=201, response_model=UserRegisterResponse)
async def register(request: CreateUserRequest):
    #DTO
    dto = CustomerRegisterDTO(
        email=request.email,
        password=request.password,
        phone=request.phone,
    )
    print(dto)
    user = await RegisterUserUseCase.excute(dto)

    return UserRegisterResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone
    )


@router.post(
    "/login", 
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
    )
async def login(
    payload: UserLoginRequest,
    request: Request
)-> Response:

    # try:
    token_response, refresh_token, family_id = await UserLoginUseCase.login(payload, request)
    # except AuthError as exc:
    #     raise HTTPException(status_code=exc.status_code, detail=exc.message)
    
    response = JSONResponse(
        content=token_response.model_dump(mode="json"),
        status_code=status.HTTP_200_OK
    )
    _set_refresh_token_cookie(response, refresh_token)
    return response



@router.post(
    "/logout",
    response_model = MessageResponse,
    status_code=status.HTTP_200_OK
)
async def logout(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=_COOKIE_NAME)
)-> Response:

    await UserLoginUseCase.logout(refresh_token)
    response = JSONResponse(
        content={"message": "Logout successful"},
        status_code=status.HTTP_200_OK
    )
    _clear_refresh_cookie(response)
    return response
    

