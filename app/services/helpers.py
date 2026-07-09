from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User


def filter_for_user(statement: Select, model, current_user: User):
    if current_user.role.value == "admin":
        return statement
    return statement.where(model.user_id == current_user.id)


def get_object_or_404(db: Session, model, object_id: UUID, current_user: User):
    statement = filter_for_user(select(model).where(model.id == object_id), model, current_user)
    obj = db.scalar(statement)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
    return obj


def ensure_email_unique(db: Session, email: str, exclude_user_id: UUID | None = None) -> None:
    statement = select(User).where(User.email == email)
    if exclude_user_id:
        statement = statement.where(User.id != exclude_user_id)
    if db.scalar(statement):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


def validate_category(db: Session, category_id: UUID | None, current_user: User) -> Category | None:
    if category_id is None:
        return None

    statement = select(Category).where(Category.id == category_id)
    if current_user.role.value != "admin":
        statement = statement.where(Category.user_id == current_user.id)

    category = db.scalar(statement)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category
