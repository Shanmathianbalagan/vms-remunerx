from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_admin
from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("/search", response_model=list[EmployeeResponse])
def search_employees(
    q: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    if not q or len(q.strip()) < 2:
        return []

    term = f"%{q.strip()}%"
    return (
        db.query(Employee)
        .filter(
            or_(
                Employee.name.ilike(term),
                Employee.email.ilike(term),
                Employee.phone.ilike(term),
            )
        )
        .order_by(Employee.name)
        .limit(20)
        .all()
    )


@router.post("", response_model=EmployeeResponse)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    existing = db.query(Employee).filter(Employee.email == payload.email).first()
    if existing:
        return existing

    employee = Employee(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        department=payload.department or "General",
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
