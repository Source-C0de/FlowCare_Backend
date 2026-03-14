from __future__ import annotations
from app.common import BaseModel
from fastapi import Query
from typing import Optional


class PaginationRequest(BaseModel):
    page: int
    limit: int 
    offset : Optional[int] | None   


def pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
)-> PaginationRequest:

    offset = (page-1)*limit
    return PaginationRequest(
        page=page,
        limit=limit,
        offset=offset
    )
