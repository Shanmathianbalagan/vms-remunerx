from datetime import datetime
from pydantic import BaseModel


class InvitationResponse(BaseModel):
    invitation_id: int
    visit_id: int
    qr_code: str
    qr_image: str
    sent_at: datetime | None = None
    expires_at: datetime
    status: str
