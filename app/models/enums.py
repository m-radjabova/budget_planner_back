import enum

from sqlalchemy import Enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class EntryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class DebtStatus(str, enum.Enum):
    ACTIVE = "active"
    PAID = "paid"


class RecurringFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class NotificationType(str, enum.Enum):
    BUDGET = "budget"
    DEBT = "debt"
    SAVING = "saving"
    SYSTEM = "system"


def sql_enum(enum_class: type[enum.Enum], name: str) -> Enum:
    return Enum(enum_class, name=name, values_callable=lambda values: [item.value for item in values])
