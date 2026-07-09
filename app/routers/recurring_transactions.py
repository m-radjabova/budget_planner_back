from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionRead,
    RecurringTransactionUpdate,
)
from app.services.recurring_transaction_service import (
    create_recurring_transaction,
    delete_recurring_transaction,
    get_recurring_transaction,
    list_recurring_transactions,
    update_recurring_transaction,
)

router = APIRouter(prefix="/recurring-transactions", tags=["Recurring Transactions"])


@router.get("/", response_model=list[RecurringTransactionRead])
def read_recurring_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_recurring_transactions(db, current_user)


@router.post("/", response_model=RecurringTransactionRead, status_code=status.HTTP_201_CREATED)
def create_new_recurring_transaction(
    payload: RecurringTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_recurring_transaction(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{recurring_id}", response_model=RecurringTransactionRead)
def read_recurring_transaction(
    recurring_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_recurring_transaction(db, current_user, recurring_id)


@router.patch("/{recurring_id}", response_model=RecurringTransactionRead)
def edit_recurring_transaction(
    recurring_id: UUID,
    payload: RecurringTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_recurring_transaction(db, current_user, recurring_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recurring_transaction(
    recurring_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_recurring_transaction(db, current_user, recurring_id)
