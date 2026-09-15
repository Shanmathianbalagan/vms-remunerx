from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_admin
from app.models.approval import Approval
from app.models.user import User
from app.models.visit import Visit
from app.schemas.approval import ApprovalDecision, ApprovalResponse
from app.services.approval_service import decide_approval

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


@router.get("", response_model=list[ApprovalResponse])
def list_approvals(
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    query = db.query(Approval).options(
        joinedload(Approval.visit).joinedload(Visit.visitor),
        joinedload(Approval.visit).joinedload(Visit.location),
    )

    if status:
        query = query.filter(Approval.status == status)

    return query.order_by(Approval.created_at.desc()).all()


@router.post("/{approval_id}/decide", response_model=ApprovalResponse)
def decide_approval_route(
    approval_id: int,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return decide_approval(
        db, approval_id, current_admin.employee_id, payload.status, payload.comments
    )
