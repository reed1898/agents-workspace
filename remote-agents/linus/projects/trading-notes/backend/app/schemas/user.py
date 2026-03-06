from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """Schema for user in database"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


class User(UserInDB):
    """Schema for user response"""
    pass


class Token(BaseModel):
    """Schema for authentication tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[str] = None
