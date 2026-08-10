"""
===============================================================================
SCHEMAS: USER & AUTHENTICATION
===============================================================================
Pydantic schemas for user signup, login, auth tokens, and profile management.
===============================================================================
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """Base fields shared across user models."""
    email: str = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name of the user")


class UserCreate(UserBase):
    """Schema required for user registration."""
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")


class UserLogin(BaseModel):
    """Schema required for user authentication."""
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResetPassword(BaseModel):
    """Schema required for requesting a password reset email."""
    email: str = Field(..., description="User email address")


class UserResponse(UserBase):
    """Schema returned for user details."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Supabase Auth UUID of the user")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Account last update timestamp")


class AuthTokenResponse(BaseModel):
    """Schema returned upon successful authentication login/signup."""
    user_id: str = Field(..., description="Unique User ID")
    email: str = Field(..., description="User email address")
    access_token: Optional[str] = Field(None, description="JWT session access token")
    token_type: str = Field("bearer", description="Token authorization type")
