from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
from app.services.notification_service import (
    create_notification,
    delete_notification,
    get_notification,
    list_notifications,
    mark_all_notifications_as_read,
    update_notification,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[NotificationRead])
def read_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_notifications(db, current_user)


@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_new_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_notification(db, current_user, payload)


@router.post("/mark-all-read")
def mark_all_read(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_count = mark_all_notifications_as_read(db, current_user)
    return {"updated_count": updated_count}


@router.get("/{notification_id}", response_model=NotificationRead)
def read_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_notification(db, current_user, notification_id)


@router.patch("/{notification_id}", response_model=NotificationRead)
def edit_notification(
    notification_id: UUID,
    payload: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_notification(db, current_user, notification_id, payload)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_notification(db, current_user, notification_id)
