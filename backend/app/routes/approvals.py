from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import CurrentUser, get_current_admin
from app.models.approval import Approval
from app.models.visit import Visit
from app.schemas.approval import ApprovalDecision, ApprovalResponse, ApprovalVisitSummary
from app.schemas.visit import VisitorSummary
from app.services.approval_service import decide_approval

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


def _build_approval_responses(approvals: list[Approval]) -> list[ApprovalResponse]:
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
                location={"name": a.visit.locations},
            ),
        )
        for a in approvals
    ]


@router.get("", response_model=list[ApprovalResponse])
def list_approvals(
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    current_admin: CurrentUser = Depends(get_current_admin),
):
    query = (
        db.query(Approval)
        .join(Visit)
        .options(joinedload(Approval.visit).joinedload(Visit.visitor))
        .filter(Visit.tenantid == current_admin.tenantid)
    )

    if status:
        query = query.filter(Approval.status == status)

    approvals = query.order_by(Approval.created_at.desc()).all()
    return _build_approval_responses(approvals)


@router.post("/{approval_id}/decide", response_model=ApprovalResponse)
def decide_approval_route(
    approval_id: int,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_admin: CurrentUser = Depends(get_current_admin),
):
    approval = decide_approval(db, approval_id, int(current_admin.sub), payload.status, payload.comments)
    return _build_approval_responses([approval])[0]
