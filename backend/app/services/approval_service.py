from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.models.visit import Visit


def create_approval(db: Session, visit: Visit) -> Approval:
    approval = Approval(visit_id=visit.visit_id, status="PENDING")
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval


def decide_approval(
    db: Session, approval_id: int, approver_employee_id: int, new_status: str, comments: str | None
) -> Approval:
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")

    if approval.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This approval has already been decided",
        )

    approval.status = new_status
    approval.comments = comments
    approval.approver_id = approver_employee_id
    approval.decided_at = datetime.utcnow()

    approval.visit.status = new_status

    db.commit()
    db.refresh(approval)
    return approval
