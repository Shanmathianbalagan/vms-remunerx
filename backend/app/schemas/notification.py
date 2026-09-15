from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    notification_id: int
    visit_id: int
    type: str
    channel: str
    recipient: str | None = None
    status: str
    created_at: datetime
    sent_at: datetime | None = None

    class Config:
        from_attributes = True
