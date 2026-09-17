from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_admin
from app.models.approval import Approval
from app.models.location import Location
from app.models.user import User
from app.models.visit import Visit
from app.schemas.approval import ApprovalDecision, ApprovalResponse, ApprovalVisitSummary
from app.schemas.visit import LocationSummary, VisitorSummary
from app.services.approval_service import decide_approval
from app.services.location_lookup import resolve_names

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


def _build_approval_responses(db: Session, approvals: list[Approval]) -> list[ApprovalResponse]:
    location_names = resolve_names(db, "LOCATION", Location, {a.visit.location_id for a in approvals})

    return [
        ApprovalResponse(
            approval_id=a.approval_id,
            status=a.status,
            comments=a.comments,
            created_at=a.created_at,
            decided_at=a.decided_at,
            visit=ApprovalVisitSummary(
                visit_id=a.visit.visit_id,
                purpose=a.visit.purpose,
                start_date=a.visit.start_date,
                end_date=a.visit.end_date,
                start_time=a.visit.start_time,
                end_time=a.visit.end_time,
                status=a.visit.status,
                visitor=VisitorSummary.model_validate(a.visit.visitor),
                location=LocationSummary(
                    location_id=a.visit.location_id,
                    name=location_names.get(a.visit.location_id, "Unknown location"),
                ),
            ),
        )
        for a in approvals
    ]


@router.get("", response_model=list[ApprovalResponse])
def list_approvals(
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    query = db.query(Approval).options(
        joinedload(Approval.visit).joinedload(Visit.visitor),
    )

    if status:
        query = query.filter(Approval.status == status)

    approvals = query.order_by(Approval.created_at.desc()).all()
    return _build_approval_responses(db, approvals)


@router.post("/{approval_id}/decide", response_model=ApprovalResponse)
def decide_approval_route(
    approval_id: int,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    approval = decide_approval(
        db, approval_id, current_admin.employee_id, payload.status, payload.comments
    )
    return _build_approval_responses(db, [approval])[0]
