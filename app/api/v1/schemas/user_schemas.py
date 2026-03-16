"""User API schemas — request/response models."""

from __future__ import annotations
from app.common import *
from fastapi import Form, File

class CreateUserRequest(BaseModel):
    email: str = Form(...)
    password: str = Form(...)
    phone: Optional[str] = Form(None)
    id_image: UploadFile = File(..., description="Required customer id image")


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

class StaffRegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    full_name: str
    role: str
    phone: Optional[str] = None
    branch_id: str

class StaffRegisterResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    phone: Optional[str] = None
    branch_id: str


__all__ = [
    "CreateUserRequest",
    "UserLoginRequest",
    "UserRegisterResponse",
    "UserLoginResponse",
    "StaffRegisterRequest",
    "StaffRegisterResponse",
]