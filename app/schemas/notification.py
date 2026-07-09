from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import NotificationType
from app.schemas.common import ORMModel


class NotificationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=1)
    type: NotificationType | None = None
    is_read: bool = False


class NotificationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    message: str | None = None
    type: NotificationType | None = None
    is_read: bool | None = None


class NotificationRead(ORMModel):
    id: UUID
    user_id: UUID
    title: str
    message: str
    type: NotificationType | None
    is_read: bool
    created_at: datetime
