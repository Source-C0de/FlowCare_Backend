"""User API schemas — request/response models."""

from __future__ import annotations
from app.common import Optional, BaseModel

class CreateUserRequest(BaseModel):
    email: str
    password: str
    phone: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserRegisterResponse(BaseModel):
    id: str
    email: str
    phone: Optional[str] = None


class UserLoginResponse(BaseModel):
    status: str
    message: str
    id: str
    email: str
