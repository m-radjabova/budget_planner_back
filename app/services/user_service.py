from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.helpers import ensure_email_unique
from app.utils.imagekit import upload_avatar_to_imagekit


ALLOWED_CURRENCIES = {"USD", "UZS", "EUR", "RUB"}


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


def create_user(db: Session, payload: UserCreate) -> User:
    ensure_email_unique(db, payload.email)
    validate_preferences(payload.currency)
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        currency=payload.currency,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_or_404(db: Session, user_id: UUID) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def validate_preferences(currency: str | None) -> None:
    if currency and currency not in ALLOWED_CURRENCIES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported currency")


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    data = payload.model_dump(exclude_unset=True)
    if "email" in data:
        ensure_email_unique(db, data["email"], exclude_user_id=user.id)

    validate_preferences(data.get("currency"))

    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def upload_avatar(db: Session, user: User, file: UploadFile) -> User:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image files are allowed")

    user.avatar_url = upload_avatar_to_imagekit(file)
    db.commit()
    db.refresh(user)
    return user
