
from __future__ import annotations

from app.common import *


from pydantic import ConfigDict

class BranchDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
    city: str
    address: str
    phone: str
    timezone: str | None = None

    
class CreateBranchRequest(BaseModel):
    name: str
    city: str
    address: str
    phone: str
    timezone: str | None = None


class BranchResponse(BaseModel):
    status: str
    message: str
    data: BranchDetails


class UpdateBranchRequest(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None

class UpdateBranchResponse(BaseModel):
    status: str
    message: str
    data: BranchDetails


__all__ = [
    "BranchDetails",
    "CreateBranchRequest",
    "BranchResponse",
    "UpdateBranchRequest",
    "UpdateBranchResponse"
]
