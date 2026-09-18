import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.badge import Badge
from app.models.invitation import Invitation
from app.models.payroll_employee import PayrollEmployee
from app.models.visit import Visit
from app.models.visit_event import VisitEvent
from app.services.notification_service import create_notification


def _get_visit_by_code(db: Session, code: str) -> Visit:
    invitation = db.query(Invitation).filter(Invitation.qr_code == code).first()
    if invitation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invitation code")

    return (
        db.query(Visit)
        .options(joinedload(Visit.visitor))
        .filter(Visit.visit_id == invitation.visit_id)
        .first()
    )


def _last_event(db: Session, visit_id: int) -> VisitEvent | None:
    # Ordered by the auto-increment id, not event_time: MySQL's default TIMESTAMP
    # resolution is 1 second, so two events in the same second would otherwise
    # sort unreliably.
    return (
        db.query(VisitEvent)
        .filter(VisitEvent.visit_id == visit_id)
        .order_by(VisitEvent.visit_event_id.desc())
        .first()
    )


def _notify_host_of_checkin(db: Session, visit: Visit) -> None:
    host = (
        db.query(PayrollEmployee)
        .filter(PayrollEmployee.empid == visit.empid, PayrollEmployee.tenantid == visit.tenantid)
        .first()
    )
    if host is None:
        return

    if host.email:
        create_notification(db, visit, "CHECK_IN_NOTIFICATION", channel="EMAIL", recipient=host.email)
    if host.phoneno:
        create_notification(db, visit, "CHECK_IN_NOTIFICATION", channel="WHATSAPP", recipient=host.phoneno)


def perform_check_in(db: Session, visit: Visit, recorded_by: str) -> tuple[VisitEvent, Badge]:
    """Core check-in logic, shared by the QR check-in endpoint and the
    walk-in auto-check-in done right after an admin creates a walk-in visit."""
    if visit.status in ("REJECTED", "CANCELLED"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This visit was {visit.status.lower()} and cannot be checked in",
        )

    last_event = _last_event(db, visit.visit_id)
    if last_event is not None and last_event.event_type == "CHECK_IN":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visitor already checked in")

    event = VisitEvent(
        visit_id=visit.visit_id,
        event_type="CHECK_IN",
        recorded_by=recorded_by,
    )
    db.add(event)

    badge = Badge(
        visit_id=visit.visit_id,
        badge_code=f"B-{visit.visit_id}-{uuid.uuid4().hex[:6].upper()}",
        status="ISSUED",
    )
    db.add(badge)

    db.commit()
    db.refresh(event)
    db.refresh(badge)

    _notify_host_of_checkin(db, visit)

    return event, badge


def check_in(db: Session, code: str, recorded_by: str) -> tuple[Visit, VisitEvent, Badge]:
    visit = _get_visit_by_code(db, code)
    event, badge = perform_check_in(db, visit, recorded_by)
    return visit, event, badge


def check_out(db: Session, code: str, recorded_by: str) -> tuple[Visit, VisitEvent, Badge]:
    visit = _get_visit_by_code(db, code)

    last_event = _last_event(db, visit.visit_id)
    if last_event is None or last_event.event_type != "CHECK_IN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visitor is not currently checked in",
        )

    event = VisitEvent(
        visit_id=visit.visit_id,
        event_type="CHECK_OUT",
        recorded_by=recorded_by,
    )
    db.add(event)

    badge = (
        db.query(Badge)
        .filter(Badge.visit_id == visit.visit_id)
        .order_by(Badge.badge_id.desc())
        .first()
    )
    badge.status = "RETURNED"

    visit.status = "COMPLETED"

    db.commit()
    db.refresh(event)
    db.refresh(badge)

    return visit, event, badge
