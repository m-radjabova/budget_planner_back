from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import EntryType
from app.schemas.common import ORMModel


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=30)
    type: EntryType


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=30)
    type: EntryType | None = None


class CategoryRead(ORMModel):
    id: UUID
    user_id: UUID
    name: str
    icon: str | None
    color: str | None
    type: EntryType
    created_at: datetime
