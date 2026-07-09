from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import ORMModel


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: UserRole = UserRole.USER
    currency: str = Field(default="USD", min_length=3, max_length=10)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    role: UserRole | None = None
    currency: str | None = Field(default=None, min_length=3, max_length=10)


class UserRead(ORMModel):
    id: UUID
    full_name: str
    email: EmailStr
    avatar_url: str | None
    role: UserRole
    currency: str
    created_at: datetime
    updated_at: datetime
