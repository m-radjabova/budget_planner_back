from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.savings_goal import SavingsDepositCreate, SavingsGoalCreate, SavingsGoalRead, SavingsGoalUpdate
from app.services.savings_goal_service import (
    create_savings_goal,
    add_deposit,
    delete_savings_goal,
    get_savings_goal,
    list_savings_goals,
    update_savings_goal,
)

router = APIRouter(prefix="/savings-goals", tags=["Savings Goals"])


@router.get("/", response_model=list[SavingsGoalRead])
def read_savings_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_savings_goals(db, current_user)


@router.post("/", response_model=SavingsGoalRead, status_code=status.HTTP_201_CREATED)
def create_new_savings_goal(
    payload: SavingsGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_savings_goal(db, current_user, payload)


@router.post("/{goal_id}/deposits", response_model=SavingsGoalRead)
def create_savings_deposit(
    goal_id: UUID,
    payload: SavingsDepositCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_deposit(db, current_user, goal_id, payload.amount)


@router.get("/{goal_id}", response_model=SavingsGoalRead)
def read_savings_goal(goal_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_savings_goal(db, current_user, goal_id)


@router.patch("/{goal_id}", response_model=SavingsGoalRead)
def edit_savings_goal(
    goal_id: UUID,
    payload: SavingsGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_savings_goal(db, current_user, goal_id, payload)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_savings_goal(goal_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_savings_goal(db, current_user, goal_id)
