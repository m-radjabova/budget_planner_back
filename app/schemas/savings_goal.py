from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class SavingsGoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    target_amount: Decimal = Field(gt=0)
    current_amount: Decimal = Field(default=0, ge=0)
    deadline: date | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=30)


class SavingsGoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    target_amount: Decimal | None = Field(default=None, gt=0)
    current_amount: Decimal | None = Field(default=None, ge=0)
    deadline: date | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=30)


class SavingsGoalRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: date | None
    icon: str | None
    color: str | None
    created_at: datetime
    updated_at: datetime
