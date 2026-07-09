from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.helpers import filter_for_user, get_object_or_404


def list_categories(db: Session, current_user: User) -> list[Category]:
    statement = filter_for_user(select(Category).order_by(Category.created_at.desc()), Category, current_user)
    return list(db.scalars(statement).all())


def create_category(db: Session, current_user: User, payload: CategoryCreate) -> Category:
    category = Category(user_id=current_user.id, **payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, current_user: User, category_id: UUID) -> Category:
    return get_object_or_404(db, Category, category_id, current_user)


def update_category(db: Session, current_user: User, category_id: UUID, payload: CategoryUpdate) -> Category:
    category = get_category(db, current_user, category_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, current_user: User, category_id: UUID) -> None:
    category = get_category(db, current_user, category_id)
    db.delete(category)
    db.commit()
