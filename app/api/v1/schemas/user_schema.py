from typing import Optional
from pydantic import BaseModel



class UserLoginRequest(BaseModel):
    email: str
    password: str 
class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str]



class UserLoginResponse(BaseModel):
    status: str
    message: str
    id: str
    email: str

class UserRegisterResponse(BaseModel):
    id: str
    name: str
    email: str


