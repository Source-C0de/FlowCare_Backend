from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class StaffCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int
    branch_id: Optional[str] = None
    phone: Optional[str] = None


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    branch_id: Optional[int] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class StaffPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    full_name: str
    email: str  
    branch_id: Optional[str]
    role_type: str
    phone: Optional[str]
    is_active: bool
    
class StaffAssign(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    staff_id: int
    service_type_id: str


class StaffAssignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    staff_id: int
    service_type_id: str

__all__ = [
    "StaffCreate",
    "StaffUpdate",
    "StaffPublic",
    "StaffAssign",
    "StaffAssignResponse",
]
