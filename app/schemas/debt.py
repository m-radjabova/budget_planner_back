from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import DebtStatus
from app.schemas.common import MONEY_MAX, Money, ORMModel


class DebtCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    total_amount: Money = Field(gt=0, le=MONEY_MAX)
    paid_amount: Money = Field(default=0, ge=0, le=MONEY_MAX)
    minimum_payment: Money | None = Field(default=None, gt=0, le=MONEY_MAX)
    due_date: date | None = None
    status: DebtStatus = DebtStatus.ACTIVE


class DebtUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    total_amount: Money | None = Field(default=None, gt=0, le=MONEY_MAX)
    paid_amount: Money | None = Field(default=None, ge=0, le=MONEY_MAX)
    minimum_payment: Money | None = Field(default=None, gt=0, le=MONEY_MAX)
    due_date: date | None = None
    status: DebtStatus | None = None


class DebtPaymentCreate(BaseModel):
    amount: Money = Field(gt=0, le=MONEY_MAX)


class DebtRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    total_amount: Money
    paid_amount: Money
    minimum_payment: Money | None
    due_date: date | None
    status: DebtStatus
    created_at: datetime
    updated_at: datetime
