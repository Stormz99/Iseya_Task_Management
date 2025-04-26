from pydantic import BaseModel, EmailStr
from typing import Optional

# For Registering User
class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"  # The default role is 'user'

# For Logging In User
class LoginSchema(BaseModel):
    email: str
    password: str

# For Access Token
class Token(BaseModel):
    access_token: str
    token_type: str
