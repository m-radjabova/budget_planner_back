from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.enums import EntryType, NotificationType
from app.models.notification import Notification
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.helpers import filter_for_user, get_object_or_404, validate_category

BUDGET_ALERT_PREFIX = "Budget Alert: "


def list_transactions(db: Session, current_user: User) -> list[Transaction]:
    statement = filter_for_user(select(Transaction).order_by(Transaction.transaction_date.desc()), Transaction, current_user)
    return list(db.scalars(statement).all())


def _get_period_bounds(month: int, year: int) -> tuple[date, date]:
    period_start = date(year, month, 1)
    if month == 12:
        period_end = date(year + 1, 1, 1)
    else:
        period_end = date(year, month + 1, 1)
    return period_start, period_end


def _sync_budget_alerts(db: Session, current_user: User) -> None:
    budgets = db.scalars(select(Budget).where(Budget.user_id == current_user.id)).all()
    active_titles: set[str] = set()

    for budget in budgets:
        if not budget.category_id:
            continue

        category = db.get(Category, budget.category_id)
        category_name = category.name if category else "Category"
        period_start, period_end = _get_period_bounds(budget.month, budget.year)

        spent = db.scalar(
            select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                Transaction.user_id == current_user.id,
                Transaction.category_id == budget.category_id,
                Transaction.type == EntryType.EXPENSE,
                Transaction.transaction_date >= period_start,
                Transaction.transaction_date < period_end,
            )
        )
        spent_value = float(spent or 0)
        limit_value = float(budget.limit_amount)
        progress = round((spent_value / limit_value) * 100) if limit_value > 0 else 0
        title = f"{BUDGET_ALERT_PREFIX}{category_name}"

        if progress >= 80:
            active_titles.add(title)
            message = f"You have used {progress}% of your {category_name} budget."
            existing_notification = db.scalar(
                select(Notification).where(
                    Notification.user_id == current_user.id,
                    Notification.type == NotificationType.BUDGET,
                    Notification.title == title,
                )
            )
            if existing_notification:
                existing_notification.message = message
                existing_notification.is_read = False
            else:
                db.add(
                    Notification(
                        user_id=current_user.id,
                        title=title,
                        message=message,
                        type=NotificationType.BUDGET,
                        is_read=False,
                    )
                )

    existing_budget_notifications = db.scalars(
        select(Notification).where(
            Notification.user_id == current_user.id,
            Notification.type == NotificationType.BUDGET,
            Notification.title.like(f"{BUDGET_ALERT_PREFIX}%"),
        )
    ).all()

    for notification in existing_budget_notifications:
        if notification.title not in active_titles:
            db.delete(notification)


def create_transaction(db: Session, current_user: User, payload: TransactionCreate) -> Transaction:
    category = validate_category(db, payload.category_id, current_user)
    if category and category.type != payload.type:
        raise ValueError("Category type and transaction type must match")

    transaction = Transaction(user_id=current_user.id, **payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    _sync_budget_alerts(db, current_user)
    db.commit()
    return transaction


def get_transaction(db: Session, current_user: User, transaction_id: UUID) -> Transaction:
    return get_object_or_404(db, Transaction, transaction_id, current_user)


def update_transaction(db: Session, current_user: User, transaction_id: UUID, payload: TransactionUpdate) -> Transaction:
    transaction = get_transaction(db, current_user, transaction_id)
    data = payload.model_dump(exclude_unset=True)
    category_id = data.get("category_id", transaction.category_id)
    entry_type = data.get("type", transaction.type)
    category = validate_category(db, category_id, current_user)
    if category and category.type != entry_type:
        raise ValueError("Category type and transaction type must match")

    for field, value in data.items():
        setattr(transaction, field, value)
    db.commit()
    db.refresh(transaction)
    _sync_budget_alerts(db, current_user)
    db.commit()
    return transaction


def delete_transaction(db: Session, current_user: User, transaction_id: UUID) -> None:
    transaction = get_transaction(db, current_user, transaction_id)
    db.delete(transaction)
    db.commit()
    _sync_budget_alerts(db, current_user)
    db.commit()
