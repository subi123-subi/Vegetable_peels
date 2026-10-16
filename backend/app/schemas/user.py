from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    preferred_language: str = Field("en", pattern="^(en|ta)$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role_name: str = "user"
    is_active: bool
    is_superuser: bool
    preferred_language: str
    created_at: datetime


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    preferred_language: Optional[str] = Field(None, pattern="^(en|ta)$")


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str = Field(..., min_length=6, max_length=100)


class UserHistoryItem(BaseModel):
    scan_id: int
    image_path: str
    vegetable_slug: Optional[str]
    vegetable_name_en: str
    vegetable_name_ta: str
    confidence: float
    is_confirmed: bool
    confirmed_weight_grams: Optional[float]
    scanned_at: datetime
