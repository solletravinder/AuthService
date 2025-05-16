from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data embedded in JWT"""
    email: Optional[str] = None

class UserBase(BaseModel):
    """Base user model (input)"""
    email: str

class UserCreate(UserBase):
    """User creation (registration)"""
    password: str = Field(..., min_length=8, max_length=64)
    full_name: Optional[str] = None

class UserOAuthCreate(UserBase):
    """OAuth user creation"""
    provider: str  # e.g., "google"

class UserUpdate(BaseModel):
    """User update fields"""
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None

class UserInDB(UserBase):
    """Complete user model (output)"""
    id: int
    is_active: bool
    hashed_password: str
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "is_active": True,
                "last_seen": "2023-01-01T00:00:00"
            }
        }
