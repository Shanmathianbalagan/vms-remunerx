from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_employee, get_current_user
from app.models.employee import Employee
from app.models.location import Location
from app.models.meeting_room import MeetingRoom
from app.models.user import User
from app.models.invitation import Invitation
from app.models.notification import Notification
from app.models.visit import Visit
from app.models.visitor import Visitor
from app.schemas.invitation import InvitationResponse
from app.schemas.notification import NotificationResponse
from app.schemas.visit import HostSummary, LocationSummary, MeetingRoomSummary, VisitCreate, VisitorSummary, VisitResponse
from app.services.invitation_service import build_qr_image_data_uri
from app.services.location_lookup import resolve_names
from app.services.visit_service import create_visit

router = APIRouter(prefix="/api/visits", tags=["visits"])


def _get_visible_visit(db: Session, visit_id: int, current_user: User, current_employee: Employee) -> Visit:
    # Admins can view any visit (e.g. one they just created on behalf of another
    # employee) - everyone else can only view visits they host themselves.
    query = db.query(Visit).filter(Visit.visit_id == visit_id)
    if current_user.role != "ADMIN":
        query = query.filter(Visit.employee_id == current_employee.employee_id)

    visit = query.first()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    return visit


def _build_visit_responses(db: Session, visits: list[Visit]) -> list[VisitResponse]:
    location_names = resolve_names(db, "LOCATION", Location, {v.location_id for v in visits})
    room_names = resolve_names(
        db, "MEETING ROOM", MeetingRoom, {v.meeting_room_id for v in visits if v.meeting_room_id}
    )

    responses = []
    for visit in visits:
        responses.append(
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
                location=LocationSummary(
                    location_id=visit.location_id,
                    name=location_names.get(visit.location_id, "Unknown location"),
                ),
                meeting_room=(
                    MeetingRoomSummary(
                        meeting_room_id=visit.meeting_room_id,
                        name=room_names.get(visit.meeting_room_id, "Unknown room"),
                    )
                    if visit.meeting_room_id
                    else None
                ),
                employee=HostSummary.model_validate(visit.employee),
            )
        )
    return responses


@router.get("", response_model=list[VisitResponse])
def list_visits(
    search: str | None = None,
    on_date: date | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_employee: Employee = Depends(get_current_employee),
):
    query = db.query(Visit).options(joinedload(Visit.visitor), joinedload(Visit.employee))

    if current_user.role != "ADMIN":
        query = query.filter(Visit.employee_id == current_employee.employee_id)

    if search:
        query = query.join(Visitor).filter(Visitor.name.ilike(f"%{search}%"))

    if on_date:
        query = query.filter(Visit.start_date <= on_date, Visit.end_date >= on_date)

    if status:
        query = query.filter(Visit.status == status)

    visits = query.order_by(Visit.start_date.desc(), Visit.start_time.desc()).all()
    return _build_visit_responses(db, visits)


@router.post("", response_model=VisitResponse)
def create_visit_route(
    payload: VisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_employee: Employee = Depends(get_current_employee),
):
    is_admin = current_user.role == "ADMIN"
    visit = create_visit(db, current_employee.employee_id, payload, is_admin=is_admin)
    return _build_visit_responses(db, [visit])[0]


@router.get("/{visit_id}/invitation", response_model=InvitationResponse)
def get_visit_invitation(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_employee: Employee = Depends(get_current_employee),
):
    _get_visible_visit(db, visit_id, current_user, current_employee)

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
    current_user: User = Depends(get_current_user),
    current_employee: Employee = Depends(get_current_employee),
):
    _get_visible_visit(db, visit_id, current_user, current_employee)

    return (
        db.query(Notification)
        .filter(Notification.visit_id == visit_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
