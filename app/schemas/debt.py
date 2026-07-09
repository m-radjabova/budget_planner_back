from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import DebtStatus
from app.schemas.common import ORMModel


class DebtCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    total_amount: Decimal = Field(gt=0)
    paid_amount: Decimal = Field(default=0, ge=0)
    minimum_payment: Decimal | None = Field(default=None, gt=0)
    due_date: date | None = None
    status: DebtStatus = DebtStatus.ACTIVE


class DebtUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    total_amount: Decimal | None = Field(default=None, gt=0)
    paid_amount: Decimal | None = Field(default=None, ge=0)
    minimum_payment: Decimal | None = Field(default=None, gt=0)
    due_date: date | None = None
    status: DebtStatus | None = None


class DebtRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    total_amount: Decimal
    paid_amount: Decimal
    minimum_payment: Decimal | None
    due_date: date | None
    status: DebtStatus
    created_at: datetime
    updated_at: datetime
