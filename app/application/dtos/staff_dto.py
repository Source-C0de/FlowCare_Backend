from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class CreateStaffDTO:
    name: str
    email: EmailStr
    password: str
    role_id: int
    branch_id: Optional[int] = None
    phone: Optional[str] = None


@dataclass
class StaffUpdateDTO:
    name: Optional[str] = None
    branch_id: Optional[int] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class StaffPublicDTO:
    id: int
    name: str
    email: str  
    branch_id: Optional[int]
    role_id: int
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


@dataclass
class StaffAssignDTO:
    staff_id: int
    service_type_id: str


__all__ = [
    "CreateStaffDTO",
    "StaffUpdateDTO",
    "StaffPublicDTO",
    "StaffAssignDTO",
]   
