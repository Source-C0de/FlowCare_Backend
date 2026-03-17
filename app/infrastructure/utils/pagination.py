from pydantic import BaseModel, Field
from fastapi import Query
from typing import Optional


class PaginationRequest(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    limit: int = Field(10, ge=1, le=100, description="Items per page")
    term: Optional[str] = Field(None, description="Search keyword")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


def pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    term: Optional[str] = Query(None),
) -> PaginationRequest:
    return PaginationRequest(
        page=page,
        limit=limit,
        term=term
    )