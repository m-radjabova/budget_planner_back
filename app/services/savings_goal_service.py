from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal
from app.models.user import User
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalUpdate
from app.services.helpers import filter_for_user, get_object_or_404


def list_savings_goals(db: Session, current_user: User) -> list[SavingsGoal]:
    statement = filter_for_user(select(SavingsGoal).order_by(SavingsGoal.created_at.desc()), SavingsGoal, current_user)
    return list(db.scalars(statement).all())


def create_savings_goal(db: Session, current_user: User, payload: SavingsGoalCreate) -> SavingsGoal:
    goal = SavingsGoal(user_id=current_user.id, **payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def get_savings_goal(db: Session, current_user: User, goal_id: UUID) -> SavingsGoal:
    return get_object_or_404(db, SavingsGoal, goal_id, current_user)


def update_savings_goal(db: Session, current_user: User, goal_id: UUID, payload: SavingsGoalUpdate) -> SavingsGoal:
    goal = get_savings_goal(db, current_user, goal_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


def delete_savings_goal(db: Session, current_user: User, goal_id: UUID) -> None:
    goal = get_savings_goal(db, current_user, goal_id)
    db.delete(goal)
    db.commit()
