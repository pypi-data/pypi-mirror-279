import enum
from datetime import datetime

from sqlmodel import Field

from systema.base import BaseModel, CreatedAtMixin, IdMixin


class NotificationStatus(str, enum.Enum):
    CREATED = "created"
    SENT = "posted"
    ERROR = "error"


class Notification(BaseModel, IdMixin, CreatedAtMixin, table=True):
    title: str
    message: str
    status: NotificationStatus = NotificationStatus.CREATED
    sent_at: datetime | None = None
    user_id: str = Field(..., foreign_key="user.id")
