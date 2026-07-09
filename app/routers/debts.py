from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.debt import DebtCreate, DebtRead, DebtUpdate
from app.services.debt_service import create_debt, delete_debt, get_debt, list_debts, update_debt

router = APIRouter(prefix="/debts", tags=["Debts"])


@router.get("/", response_model=list[DebtRead])
def read_debts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_debts(db, current_user)


@router.post("/", response_model=DebtRead, status_code=status.HTTP_201_CREATED)
def create_new_debt(
    payload: DebtCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_debt(db, current_user, payload)


@router.get("/{debt_id}", response_model=DebtRead)
def read_debt(debt_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_debt(db, current_user, debt_id)


@router.patch("/{debt_id}", response_model=DebtRead)
def edit_debt(
    debt_id: UUID,
    payload: DebtUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_debt(db, current_user, debt_id, payload)


@router.delete("/{debt_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_debt(debt_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_debt(db, current_user, debt_id)
