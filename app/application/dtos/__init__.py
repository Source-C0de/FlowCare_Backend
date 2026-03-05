from pydantic import BaseModel, EmailStr, Field
from typing import Optional , List
from datetime import datetime



#Auth
class CustomerRegisterDTO(BaseModel):
    email: EmailStr
    phone: Optional[str]
    password: str =  Field(min_length=6)
    full_name: str
    register_date: datetime
    
    model_config = {"from_attributes": True}
