from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import create_category, delete_category, get_category, list_categories, update_category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
def read_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_categories(db, current_user)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_new_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(db, current_user, payload)


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_category(db, current_user, category_id)


@router.patch("/{category_id}", response_model=CategoryRead)
def edit_category(
    category_id: UUID,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_category(db, current_user, category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_category(category_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_category(db, current_user, category_id)
