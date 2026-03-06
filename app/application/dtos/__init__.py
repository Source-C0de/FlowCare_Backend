from token import OP
from pydantic import BaseModel, EmailStr, Field
from typing import Optional , List
from datetime import datetime
from dataclasses import dataclass


#Auth
class CustomerRegisterDTO(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str]
