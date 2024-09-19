from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str

class UserCreate(UserBase):
    password: str
    password_confirm: str

class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True