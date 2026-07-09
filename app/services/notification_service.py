from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.services.helpers import filter_for_user, get_object_or_404


def list_notifications(db: Session, current_user: User) -> list[Notification]:
    statement = filter_for_user(
        select(Notification).order_by(Notification.created_at.desc()),
        Notification,
        current_user,
    )
    return list(db.scalars(statement).all())


def create_notification(db: Session, current_user: User, payload: NotificationCreate) -> Notification:
    notification = Notification(user_id=current_user.id, **payload.model_dump())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notification(db: Session, current_user: User, notification_id: UUID) -> Notification:
    return get_object_or_404(db, Notification, notification_id, current_user)


def update_notification(
    db: Session,
    current_user: User,
    notification_id: UUID,
    payload: NotificationUpdate,
) -> Notification:
    notification = get_notification(db, current_user, notification_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(notification, field, value)
    db.commit()
    db.refresh(notification)
    return notification


def mark_all_notifications_as_read(db: Session, current_user: User) -> int:
    notifications = list_notifications(db, current_user)
    updated_count = 0

    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
            updated_count += 1

    db.commit()
    return updated_count


def delete_notification(db: Session, current_user: User, notification_id: UUID) -> None:
    notification = get_notification(db, current_user, notification_id)
    db.delete(notification)
    db.commit()
