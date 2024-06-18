from typing import Optional

import pydantic

from .record import (
    NotificationChannel,
    ReadStatus,
)
from .validator import LifecycleStatusValidator


class UpdateNotificationRequest(pydantic.BaseModel, LifecycleStatusValidator):
    notification_id: str
    read_status: Optional[ReadStatus] = None
    lifecycle_status: Optional[dict[NotificationChannel, str]] = None
