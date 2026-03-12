"""Auth endpoints — thin controllers that delegate to use cases."""

from __future__ import annotations

from app.common import APIRouter, Cookie, Depends, Request, Response, status

from app.api.dependencies import get_login_use_case, get_logout_use_case, get_register_use_case
from app.api.v1.schemas.user_schemas import CreateUserRequest, UserRegisterResponse, UserLoginRequest
from app.api.v1.schemas.auth_schemas import TokenResponse, MessageResponse, UserPublic
from app.application.dtos.auth_dto import CustomerRegisterDTO
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.logout_user import LogoutUserUseCase
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

_COOKIE_NAME = settings.REFRESH_COOKIE_NAME


def _set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
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
async def register(
    request: CreateUserRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case),
):
    dto = CustomerRegisterDTO(
        email=request.email,
        password=request.password,
        phone=request.phone,
    )
    user = await use_case.execute(dto)
    return UserRegisterResponse(
        id=str(user.id),
        email=user.email,
        phone=user.phone,
    )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: UserLoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_use_case),
) -> Response:
    user, access_token, refresh_token, family_id = await use_case.execute(
        email=payload.email,
        password=payload.password,
    )

    token_response = TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserPublic(
            id=user.id,
            email=user.email,
            phone=user.phone,
            role=str(user.role_type or ""),
            status="active" if user.is_active else "inactive",
        ),
    )

    response = JSONResponse(
        content=token_response.model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )
    _set_refresh_token_cookie(response, refresh_token)
    return response


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    use_case: LogoutUserUseCase = Depends(get_logout_use_case),
    refresh_token: str | None = Cookie(default=None, alias=_COOKIE_NAME),
) -> Response:
    await use_case.execute(refresh_token)
    resp = JSONResponse(
        content={"message": "Logout successful"},
        status_code=status.HTTP_200_OK,
    )
    _clear_refresh_cookie(resp)
    return resp
