from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base schema for shared user fields
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Schema for Registration input
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "USER"  # Default role USER, can be "ADMIN"

# Schema for Login input
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for Token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for User Response (Password is EXCLUDED for security)
class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True