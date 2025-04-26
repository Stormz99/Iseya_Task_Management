from pydantic import BaseModel, EmailStr
from app.models.enum import RoleEnum
from typing import Optional


class RegisterSchema(BaseModel):
    username: Optional[str] = None  
    email: EmailStr
    password: str
    role: RoleEnum  


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    username: Optional[str] = None  
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True  


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
