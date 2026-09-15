import base64
import io
import uuid
from datetime import datetime

import qrcode
from sqlalchemy.orm import Session

from app.models.invitation import Invitation
from app.models.visit import Visit


def create_invitation(db: Session, visit: Visit) -> Invitation:
    invitation = Invitation(
        visit_id=visit.visit_id,
        qr_code=uuid.uuid4().hex,
        expires_at=datetime.combine(visit.end_date, visit.end_time),
        status="GENERATED",
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


def build_qr_image_data_uri(qr_code: str) -> str:
    img = qrcode.make(qr_code)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"
