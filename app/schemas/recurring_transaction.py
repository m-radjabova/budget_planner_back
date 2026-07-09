from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import EntryType, RecurringFrequency
from app.schemas.common import ORMModel


class RecurringTransactionCreate(BaseModel):
    category_id: UUID | None = None
    title: str = Field(min_length=1, max_length=150)
    amount: Decimal = Field(gt=0)
    type: EntryType
    frequency: RecurringFrequency
    start_date: date
    end_date: date | None = None
    is_active: bool = True


class RecurringTransactionUpdate(BaseModel):
    category_id: UUID | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    amount: Decimal | None = Field(default=None, gt=0)
    type: EntryType | None = None
    frequency: RecurringFrequency | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


class RecurringTransactionRead(ORMModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None
    title: str
    amount: Decimal
    type: EntryType
    frequency: RecurringFrequency
    start_date: date
    end_date: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
