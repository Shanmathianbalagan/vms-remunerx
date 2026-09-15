from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.visit import VisitCreate
from app.services.approval_service import create_approval
from app.services.invitation_service import create_invitation
from app.services.notification_service import create_notification


def create_visit(db: Session, employee_id: int, payload: VisitCreate) -> Visit:
    visitor = db.query(Visitor).filter(Visitor.visitor_id == payload.visitor_id).first()
    if visitor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")

    location = db.query(Location).filter(Location.location_id == payload.location_id).first()
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    visit = Visit(
        visitor_id=payload.visitor_id,
        employee_id=employee_id,
        location_id=payload.location_id,
        purpose=payload.purpose,
        start_date=payload.start_date,
        end_date=payload.end_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        notes=payload.notes,
        status="CREATED",
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    create_invitation(db, visit)
    create_notification(db, visit, "VISIT_INVITATION")
    create_approval(db, visit)

    return visit
