from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class BudgetCreate(BaseModel):
    category_id: UUID | None = None
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)
    limit_amount: Decimal = Field(gt=0)


class BudgetUpdate(BaseModel):
    category_id: UUID | None = None
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2000, le=2100)
    limit_amount: Decimal | None = Field(default=None, gt=0)


class BudgetRead(ORMModel):
    id: UUID
    user_id: UUID
    category_id: UUID | None
    month: int
    year: int
    limit_amount: Decimal
    created_at: datetime
    updated_at: datetime
