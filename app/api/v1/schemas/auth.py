

from __future__ import annotations


import uuid
from datetime import datetime
from typing import Any


from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator



class LoginRequest(BaseModel):
    identifier: Annotated[str, Field(min_length=3, max_length=254, examples=["user@example.com", "+966501234567"])]
    password:   Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        v = v.strip()
        if _looks_like_email(v):
            # basic email sanity
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
                raise ValueError("Invalid email format")
            return v.lower()
        if _looks_like_phone(v):
            return v
        raise ValueError("Identifier must be a valid email or E.164 phone number")



class UserPublic(BaseModel):
    id: uuid.UUID
    email: str | None
    phone: str | None
    role: str
    status: str
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}

# Response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int 
    user: UserPublic


class MessageResponse(BaseModel):
    """Generic success/info message."""
    message: str

class ErrorResponse(BaseModel):
    """
    Anti-enumeration: all auth errors use the same surface message.
    Detail is only populated in non-production environments.
    """
    error:  str
    detail: str | None = None