from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TimestampMixin(ORMModel):
    id: UUID
    created_at: datetime


class TimestampUpdateMixin(TimestampMixin):
    updated_at: datetime


class AmountMixin(BaseModel):
    amount: Decimal


class DateFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
