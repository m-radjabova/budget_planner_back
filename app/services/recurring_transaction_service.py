from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.recurring_transaction import RecurringTransaction
from app.models.user import User
from app.schemas.recurring_transaction import RecurringTransactionCreate, RecurringTransactionUpdate
from app.services.helpers import filter_for_user, get_object_or_404, validate_category


def list_recurring_transactions(db: Session, current_user: User) -> list[RecurringTransaction]:
    statement = filter_for_user(
        select(RecurringTransaction).order_by(RecurringTransaction.created_at.desc()),
        RecurringTransaction,
        current_user,
    )
    return list(db.scalars(statement).all())


def create_recurring_transaction(
    db: Session,
    current_user: User,
    payload: RecurringTransactionCreate,
) -> RecurringTransaction:
    category = validate_category(db, payload.category_id, current_user)
    if category and category.type != payload.type:
        raise ValueError("Category type and recurring transaction type must match")

    recurring = RecurringTransaction(user_id=current_user.id, **payload.model_dump())
    db.add(recurring)
    db.commit()
    db.refresh(recurring)
    return recurring


def get_recurring_transaction(db: Session, current_user: User, recurring_id: UUID) -> RecurringTransaction:
    return get_object_or_404(db, RecurringTransaction, recurring_id, current_user)


def update_recurring_transaction(
    db: Session,
    current_user: User,
    recurring_id: UUID,
    payload: RecurringTransactionUpdate,
) -> RecurringTransaction:
    recurring = get_recurring_transaction(db, current_user, recurring_id)
    data = payload.model_dump(exclude_unset=True)
    category = validate_category(db, data.get("category_id", recurring.category_id), current_user)
    entry_type = data.get("type", recurring.type)
    if category and category.type != entry_type:
        raise ValueError("Category type and recurring transaction type must match")

    for field, value in data.items():
        setattr(recurring, field, value)
    db.commit()
    db.refresh(recurring)
    return recurring


def delete_recurring_transaction(db: Session, current_user: User, recurring_id: UUID) -> None:
    recurring = get_recurring_transaction(db, current_user, recurring_id)
    db.delete(recurring)
    db.commit()
