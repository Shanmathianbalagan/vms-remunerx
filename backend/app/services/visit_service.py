from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.data_mapping import DataMapping
from app.models.payroll_employee import PayrollEmployee
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.visit import VisitCreate
from app.services.approval_service import create_approval
from app.services.checkin_service import perform_check_in
from app.services.invitation_service import create_invitation
from app.services.notification_service import create_notification


def create_visit(
    db: Session,
    creator_empid: str,
    tenantid: int,
    payload: VisitCreate,
    is_admin: bool = False,
    actor_identifier: str | None = None,
) -> Visit:
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

    meeting_room_text = ""
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
        meeting_room_text = meeting_room.internalcode

    host_empid = creator_empid
    host_employee = None
    if is_admin and payload.host_employee_id:
        host_employee = (
            db.query(PayrollEmployee)
            .filter(PayrollEmployee.empid == payload.host_employee_id, PayrollEmployee.tenantid == tenantid)
            .first()
        )
        if host_employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Host employee not found")
        host_empid = host_employee.empid

    visit = Visit(
        tenantid=tenantid,
        visitor_id=payload.visitor_id,
        empid=host_empid,
        locations=location.internalcode,
        meetingroom=meeting_room_text,
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

    invitation = create_invitation(db, visit)

    is_walkin = is_admin and host_employee is not None

    if is_walkin:
        # Visitor is already physically here - no point inviting them to a
        # visit that's already happening. Check them in immediately instead,
        # which is what actually notifies the host (visitor has arrived).
        perform_check_in(db, visit, recorded_by=actor_identifier or "ADMIN")
    else:
        create_notification(db, visit, "VISIT_INVITATION", channel="EMAIL", qr_code=invitation.qr_code)
        create_notification(db, visit, "VISIT_INVITATION", channel="WHATSAPP", qr_code=invitation.qr_code)
        if host_employee is not None and host_employee.email:
            create_notification(db, visit, "HOST_ASSIGNED", recipient=host_employee.email)

    create_approval(db, visit)

    return visit
