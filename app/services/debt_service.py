from uuid import UUID

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.debt import Debt
from app.models.enums import DebtStatus
from app.models.user import User
from app.schemas.common import quantize_money
from app.schemas.debt import DebtCreate, DebtUpdate
from app.services.helpers import filter_for_user, get_object_or_404


def list_debts(db: Session, current_user: User) -> list[Debt]:
    statement = filter_for_user(select(Debt).order_by(Debt.created_at.desc()), Debt, current_user)
    return list(db.scalars(statement).all())


def create_debt(db: Session, current_user: User, payload: DebtCreate) -> Debt:
    debt = Debt(user_id=current_user.id, **payload.model_dump())
    db.add(debt)
    db.commit()
    db.refresh(debt)
    return debt


def get_debt(db: Session, current_user: User, debt_id: UUID) -> Debt:
    return get_object_or_404(db, Debt, debt_id, current_user)


def update_debt(db: Session, current_user: User, debt_id: UUID, payload: DebtUpdate) -> Debt:
    debt = get_debt(db, current_user, debt_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(debt, field, value)
    db.commit()
    db.refresh(debt)
    return debt


def add_payment(db: Session, current_user: User, debt_id: UUID, amount: Decimal) -> Debt:
    debt = get_debt(db, current_user, debt_id)
    total_amount = quantize_money(debt.total_amount)
    paid_amount = quantize_money(debt.paid_amount)
    payment_amount = quantize_money(amount)
    remaining = total_amount - paid_amount

    if payment_amount > remaining:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payment cannot be greater than the remaining debt.",
        )

    debt.paid_amount = quantize_money(paid_amount + payment_amount)
    debt.status = DebtStatus.PAID if debt.paid_amount >= total_amount else DebtStatus.ACTIVE
    db.commit()
    db.refresh(debt)
    return debt


def delete_debt(db: Session, current_user: User, debt_id: UUID) -> None:
    debt = get_debt(db, current_user, debt_id)
    db.delete(debt)
    db.commit()
