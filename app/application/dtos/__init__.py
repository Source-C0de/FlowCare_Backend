from token import OP
from pydantic import BaseModel, EmailStr, Field
from typing import Optional , List
from datetime import datetime
from dataclasses import dataclass


#Auth
class CustomerRegisterDTO(BaseModel):
    email: str
    password: str
    phone: Optional[str]


class UserLoginDTO(BaseModel):
    email: str
    password: str


class AppointmentDTO(BaseModel):
    branch_id: str
    service_type_id: str
    staff_id: str
    start_time: str
    end_time: str