from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import CurrentUser, get_current_user
from app.models.invitation import Invitation
from app.models.notification import Notification
from app.models.payroll_employee import PayrollEmployee
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.invitation import InvitationResponse
from app.schemas.notification import NotificationResponse
from app.schemas.visit import HostSummary, VisitCreate, VisitorSummary, VisitResponse
from app.services.invitation_service import build_qr_image_data_uri
from app.services.visit_service import create_visit

router = APIRouter(prefix="/api/visits", tags=["visits"])


def _get_visible_visit(db: Session, visit_id: int, current_user: CurrentUser) -> Visit:
    # Admins can view any visit in their tenant - everyone else can only view
    # visits they host themselves.
    query = db.query(Visit).filter(Visit.visit_id == visit_id, Visit.tenantid == current_user.tenantid)
    if not current_user.is_admin:
        query = query.filter(Visit.empid == current_user.empid)

    visit = query.first()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    return visit


def _resolve_host_names(db: Session, tenantid: int, empids: set[str]) -> dict[str, str]:
    if not empids:
        return {}
    rows = (
        db.query(PayrollEmployee)
        .filter(PayrollEmployee.tenantid == tenantid, PayrollEmployee.empid.in_(empids))
        .all()
    )
    return {row.empid: row.empname for row in rows}


def _build_visit_responses(db: Session, tenantid: int, visits: list[Visit]) -> list[VisitResponse]:
    host_names = _resolve_host_names(db, tenantid, {v.empid for v in visits})

    return [
        VisitResponse(
            visit_id=visit.visit_id,
            purpose=visit.purpose,
            start_date=visit.start_date,
            end_date=visit.end_date,
            start_time=visit.start_time,
            end_time=visit.end_time,
            status=visit.status,
            notes=visit.notes,
            created_at=visit.created_at,
            visitor=VisitorSummary.model_validate(visit.visitor),
            location={"name": visit.locations},
            meeting_room={"name": visit.meetingroom} if visit.meetingroom else None,
            employee=HostSummary(employee_id=visit.empid, name=host_names.get(visit.empid, visit.empid)),
        )
        for visit in visits
    ]


@router.get("", response_model=list[VisitResponse])
def list_visits(
    search: str | None = None,
    on_date: date | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    query = (
        db.query(Visit)
        .options(joinedload(Visit.visitor))
        .filter(Visit.tenantid == current_user.tenantid)
    )

    if not current_user.is_admin:
        query = query.filter(Visit.empid == current_user.empid)

    if search:
        query = query.join(Visitor).filter(Visitor.name.ilike(f"%{search}%"))

    if on_date:
        query = query.filter(Visit.start_date <= on_date, Visit.end_date >= on_date)

    if status:
        query = query.filter(Visit.status == status)

    visits = query.order_by(Visit.start_date.desc(), Visit.start_time.desc()).all()
    return _build_visit_responses(db, current_user.tenantid, visits)


@router.post("", response_model=VisitResponse)
def create_visit_route(
    payload: VisitCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.is_admin:
        if not payload.host_employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Select the employee this visitor is here to see",
            )
        creator_empid = None
    else:
        if not current_user.empid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is not linked to an employee record",
            )
        creator_empid = current_user.empid

    visit = create_visit(
        db,
        creator_empid,
        current_user.tenantid,
        payload,
        is_admin=current_user.is_admin,
        actor_identifier=current_user.empid or current_user.sub,
    )
    return _build_visit_responses(db, current_user.tenantid, [visit])[0]


@router.get("/{visit_id}/invitation", response_model=InvitationResponse)
def get_visit_invitation(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _get_visible_visit(db, visit_id, current_user)

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
    current_user: CurrentUser = Depends(get_current_user),
):
    _get_visible_visit(db, visit_id, current_user)

    return (
        db.query(Notification)
        .filter(Notification.visit_id == visit_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
