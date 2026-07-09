from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.enums import EntryType
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate
from app.services.helpers import filter_for_user, get_object_or_404, validate_category


def list_budgets(db: Session, current_user: User) -> list[Budget]:
    statement = filter_for_user(select(Budget).order_by(Budget.year.desc(), Budget.month.desc()), Budget, current_user)
    return list(db.scalars(statement).all())


def create_budget(db: Session, current_user: User, payload: BudgetCreate) -> Budget:
    category = validate_category(db, payload.category_id, current_user)
    if category and category.type != EntryType.EXPENSE:
        raise ValueError("Budget can only be attached to an expense category")

    budget = Budget(user_id=current_user.id, **payload.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budget(db: Session, current_user: User, budget_id: UUID) -> Budget:
    return get_object_or_404(db, Budget, budget_id, current_user)


def update_budget(db: Session, current_user: User, budget_id: UUID, payload: BudgetUpdate) -> Budget:
    budget = get_budget(db, current_user, budget_id)
    data = payload.model_dump(exclude_unset=True)
    category = validate_category(db, data.get("category_id", budget.category_id), current_user)
    if category and category.type != EntryType.EXPENSE:
        raise ValueError("Budget can only be attached to an expense category")
    for field, value in data.items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, current_user: User, budget_id: UUID) -> None:
    budget = get_budget(db, current_user, budget_id)
    db.delete(budget)
    db.commit()
