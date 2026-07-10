from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import MONEY_MAX, Money, ORMModel


class BudgetCreate(BaseModel):
    category_id: UUID | None = None
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)
    limit_amount: Money = Field(gt=0, le=MONEY_MAX)


class BudgetUpdate(BaseModel):
    category_id: UUID | None = None
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2000, le=2100)
    limit_amount: Money | None = Field(default=None, gt=0, le=MONEY_MAX)


class BudgetRead(ORMModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None
    month: int
    year: int
    limit_amount: Money
    created_at: datetime
    updated_at: datetime
