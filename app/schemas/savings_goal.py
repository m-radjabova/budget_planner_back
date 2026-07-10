from datetime import date, datetime
from uuid import UUID
from decimal import Decimal



from pydantic import BaseModel, Field

from app.schemas.common import MONEY_MAX, Money, ORMModel


class SavingsGoalCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150,
        examples=["Vacation Trip"],
    )

    target_amount: Money = Field(
        gt=0,
        le=MONEY_MAX,
        examples=["25000000.00"],
    )

    current_amount: Money = Field(
        default=Decimal("0.00"),
        ge=0,
        le=MONEY_MAX,
        examples=["5000000.00"],
    )

    deadline: date | None = Field(
        default=None,
        examples=["2026-12-31"],
    )

    icon: str | None = Field(
        default=None,
        max_length=50,
        examples=["plane"],
    )

    color: str | None = Field(
        default=None,
        max_length=30,
        examples=["#8B5CF6"],
    )

class SavingsGoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    target_amount: Money | None = Field(default=None, gt=0, le=MONEY_MAX)
    current_amount: Money | None = Field(default=None, ge=0, le=MONEY_MAX)
    deadline: date | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=30)


class SavingsDepositCreate(BaseModel):
    amount: Money = Field(gt=0, le=MONEY_MAX)


class SavingsGoalRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    target_amount: Money
    current_amount: Money
    deadline: date | None
    icon: str | None
    color: str | None
    created_at: datetime
    updated_at: datetime
