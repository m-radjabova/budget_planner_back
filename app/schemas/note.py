from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str | None = None
    note_date: date | None = None


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    content: str | None = None
    note_date: date | None = None


class NoteRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    content: str | None
    note_date: date | None
    created_at: datetime
    updated_at: datetime
