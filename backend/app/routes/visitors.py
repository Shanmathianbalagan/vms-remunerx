from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_employee
from app.models.employee import Employee
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate, VisitorResponse

router = APIRouter(prefix="/api/visitors", tags=["visitors"])


@router.get("/search", response_model=list[VisitorResponse])
def search_visitors(
    q: str,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    if not q or len(q.strip()) < 2:
        return []

    term = f"%{q.strip()}%"
    return (
        db.query(Visitor)
        .filter(
            or_(
                Visitor.name.ilike(term),
                Visitor.phone.ilike(term),
                Visitor.email.ilike(term),
            )
        )
        .order_by(Visitor.name)
        .limit(20)
        .all()
    )


@router.post("", response_model=VisitorResponse)
def create_visitor(
    payload: VisitorCreate,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    existing = db.query(Visitor).filter(Visitor.phone == payload.phone).first()
    if existing:
        return existing

    visitor = Visitor(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        company=payload.company,
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor
