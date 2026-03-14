from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class AuditLogsRequest:
    page: Optional[int] | None
    limit: Optional[int] | None
    term: Optional[int] | None



__all__ = [
    "AuditLogsRequest",
]