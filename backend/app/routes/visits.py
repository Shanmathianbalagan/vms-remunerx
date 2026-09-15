from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_employee
from app.models.employee import Employee
from app.models.invitation import Invitation
from app.models.notification import Notification
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.invitation import InvitationResponse
from app.schemas.notification import NotificationResponse
from app.schemas.visit import VisitCreate, VisitResponse
from app.services.invitation_service import build_qr_image_data_uri
from app.services.visit_service import create_visit

router = APIRouter(prefix="/api/visits", tags=["visits"])


def _get_owned_visit(db: Session, visit_id: int, employee_id: int) -> Visit:
    visit = (
        db.query(Visit)
        .filter(Visit.visit_id == visit_id, Visit.employee_id == employee_id)
        .first()
    )
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    return visit


@router.get("", response_model=list[VisitResponse])
def list_visits(
    search: str | None = None,
    on_date: date | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    query = (
        db.query(Visit)
        .options(joinedload(Visit.visitor), joinedload(Visit.location))
        .filter(Visit.employee_id == current_employee.employee_id)
    )

    if search:
        query = query.join(Visitor).filter(Visitor.name.ilike(f"%{search}%"))

    if on_date:
        query = query.filter(Visit.start_date <= on_date, Visit.end_date >= on_date)

    if status:
        query = query.filter(Visit.status == status)

    return query.order_by(Visit.start_date.desc(), Visit.start_time.desc()).all()


@router.post("", response_model=VisitResponse)
def create_visit_route(
    payload: VisitCreate,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    return create_visit(db, current_employee.employee_id, payload)


@router.get("/{visit_id}/invitation", response_model=InvitationResponse)
def get_visit_invitation(
    visit_id: int,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    _get_owned_visit(db, visit_id, current_employee.employee_id)

    invitation = db.query(Invitation).filter(Invitation.visit_id == visit_id).first()
    if invitation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")

    return InvitationResponse(
        invitation_id=invitation.invitation_id,
        visit_id=invitation.visit_id,
        qr_code=invitation.qr_code,
        qr_image=build_qr_image_data_uri(invitation.qr_code),
        sent_at=invitation.sent_at,
        expires_at=invitation.expires_at,
        status=invitation.status,
    )


@router.get("/{visit_id}/notifications", response_model=list[NotificationResponse])
def get_visit_notifications(
    visit_id: int,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    _get_owned_visit(db, visit_id, current_employee.employee_id)

    return (
        db.query(Notification)
        .filter(Notification.visit_id == visit_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
