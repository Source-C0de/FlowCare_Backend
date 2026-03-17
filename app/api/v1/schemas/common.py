from __future__ import annotations

from app.common import *
from typing import TypeVar, Generic
from app.infrastructure.utils.pagination import PaginationRequest


T = TypeVar("T")

class PaginationResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    limit: int
    

class PaginationRequest(PaginationRequest):
    pass

class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int

__all__ = [
    "PaginationResponse",
    "PaginationRequest",
    "MessageResponse",
    "ErrorResponse",
]