from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserRegister, UserUpdate
from app.services.auth_service import register_user
from app.services.user_service import create_user, delete_user, get_user_or_404, list_users, update_user, upload_avatar

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.get("/", response_model=list[UserRead], dependencies=[Depends(require_admin)])
def get_users(db: Session = Depends(get_db)):
    return list_users(db)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_new_user(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, payload)


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    safe_payload = UserUpdate(**payload.model_dump(exclude={"role"}, exclude_unset=True))
    return update_user(db, current_user, safe_payload)


@router.patch("/me/avatar", response_model=UserRead)
def upload_my_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_avatar(db, current_user, file)


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_admin)])
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return get_user_or_404(db, user_id)


@router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(require_admin)])
def update_user_by_admin(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    return update_user(db, user, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def remove_user(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    delete_user(db, user)
