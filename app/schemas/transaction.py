from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import EntryType
from app.schemas.common import MONEY_MAX, Money, ORMModel


class TransactionCreate(BaseModel):
    category_id: UUID | None = None
    title: str = Field(min_length=1, max_length=150)
    amount: Money = Field(gt=0, le=MONEY_MAX)
    type: EntryType
    transaction_date: date
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class TransactionUpdate(BaseModel):
    category_id: UUID | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    amount: Money | None = Field(default=None, gt=0, le=MONEY_MAX)
    type: EntryType | None = None
    transaction_date: date | None = None
    description: str | None = None
    tags: list[str] | None = None


class TransactionRead(ORMModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None
    title: str
    amount: Money
    type: EntryType
    transaction_date: date
    description: str | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
