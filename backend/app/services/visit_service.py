from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.data_mapping import DataMapping
from app.models.employee import Employee
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.visit import VisitCreate
from app.services.approval_service import create_approval
from app.services.invitation_service import create_invitation
from app.services.notification_service import create_notification


def create_visit(db: Session, creator_employee_id: int, payload: VisitCreate, is_admin: bool = False) -> Visit:
    visitor = db.query(Visitor).filter(Visitor.visitor_id == payload.visitor_id).first()
    if visitor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visitor not found")

    location = (
        db.query(DataMapping)
        .filter(DataMapping.datamappingid == payload.location_id, DataMapping.grouping == "LOCATION")
        .first()
    )
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    if payload.meeting_room_id is not None:
        meeting_room = (
            db.query(DataMapping)
            .filter(
                DataMapping.datamappingid == payload.meeting_room_id,
                DataMapping.grouping == "MEETING ROOM",
            )
            .first()
        )
        if meeting_room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting room not found")

    host_employee_id = creator_employee_id
    host_employee = None
    if is_admin and payload.host_employee_id:
        host_employee = db.query(Employee).filter(Employee.employee_id == payload.host_employee_id).first()
        if host_employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Host employee not found")
        host_employee_id = host_employee.employee_id

    visit = Visit(
        visitor_id=payload.visitor_id,
        employee_id=host_employee_id,
        location_id=payload.location_id,
        meeting_room_id=payload.meeting_room_id,
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
    create_notification(db, visit, "VISIT_INVITATION", channel="EMAIL")
    create_notification(db, visit, "VISIT_INVITATION", channel="WHATSAPP")
    if host_employee is not None:
        create_notification(db, visit, "HOST_ASSIGNED", recipient=host_employee.email)
    create_approval(db, visit)

    return visit
