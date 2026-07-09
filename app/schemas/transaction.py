from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import EntryType
from app.schemas.common import ORMModel


class TransactionCreate(BaseModel):
    category_id: UUID | None = None
    title: str = Field(min_length=1, max_length=150)
    amount: Decimal = Field(gt=0)
    type: EntryType
    transaction_date: date
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class TransactionUpdate(BaseModel):
    category_id: UUID | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    amount: Decimal | None = Field(default=None, gt=0)
    type: EntryType | None = None
    transaction_date: date | None = None
    description: str | None = None
    tags: list[str] | None = None


class TransactionRead(ORMModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None
    title: str
    amount: Decimal
    type: EntryType
    transaction_date: date
    description: str | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
