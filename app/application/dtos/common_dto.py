from __future__ import annotations

from dataclasses import dataclass
from app.infrastructure.utils.pagination import PaginationRequest

@dataclass
class PaginationDTO(PaginationRequest):
    pass

__all__ = [
    "PaginationDTO",
]