
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class BranchDetails(BaseModel):
    name: str
    address: str
    phone: str
    is_active: bool

class CreateBranchRequest(BaseModel):
    name: str
    city: str
    address: str
    phone: str
    timezone: str | None = None


class CreateBranchResponse(BaseModel):
    status: str
    message: str
    data: BranchDetails

