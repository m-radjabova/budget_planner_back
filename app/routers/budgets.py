from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate
from app.services.budget_service import create_budget, delete_budget, get_budget, list_budgets, update_budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/", response_model=list[BudgetRead])
def read_budgets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_budgets(db, current_user)


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_new_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_budget(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{budget_id}", response_model=BudgetRead)
def read_budget(budget_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_budget(db, current_user, budget_id)


@router.patch("/{budget_id}", response_model=BudgetRead)
def edit_budget(
    budget_id: UUID,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_budget(db, current_user, budget_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_budget(budget_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_budget(db, current_user, budget_id)
