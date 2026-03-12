"""Auth API schemas — token responses, messages, errors."""

from __future__ import annotations
import uuid
from app.common import Optional, BaseModel, datetime




class UserPublic(BaseModel):
    id: uuid.UUID
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    status: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic


class MessageResponse(BaseModel):
    """Generic success/info message."""
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
