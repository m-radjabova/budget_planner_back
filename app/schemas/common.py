from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Annotated, Any
from uuid import UUID

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
)


MONEY_QUANT = Decimal("0.01")
MONEY_MAX = Decimal("9999999999.99")


def parse_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value

    return Decimal(str(value))


def quantize_money(value: Decimal) -> Decimal:
    decimal_value = parse_decimal(value)

    with localcontext() as context:
        context.prec = max(
            len(decimal_value.as_tuple().digits) + 2,
            28,
        )

        return decimal_value.quantize(
            MONEY_QUANT,
            rounding=ROUND_HALF_UP,
        )


def serialize_money(value: Decimal) -> str:
    return format(quantize_money(value), "f")


Money = Annotated[
    Decimal,
    BeforeValidator(parse_decimal),
    Field(
        max_digits=12,
        decimal_places=2,
        examples=["1000000.00"],
    ),
    AfterValidator(quantize_money),
    PlainSerializer(
        serialize_money,
        return_type=str,
        when_used="json",
    ),
]


class SchemaModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )


class ORMModel(SchemaModel):
    pass


class TimestampMixin(ORMModel):
    id: UUID
    created_at: datetime


class TimestampUpdateMixin(TimestampMixin):
    updated_at: datetime


class AmountMixin(SchemaModel):
    amount: Money


class DateFilter(SchemaModel):
    start_date: date | None = None
    end_date: date | None = None