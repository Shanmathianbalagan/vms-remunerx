import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser, get_current_admin
from app.models.payroll_employee import PayrollEmployee
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["employees"])


def _to_response(row: PayrollEmployee) -> EmployeeResponse:
    return EmployeeResponse(
        employee_id=row.empid, name=row.empname, email=row.email,
        department=row.department, phone=row.phoneno,
    )


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_admin: CurrentUser = Depends(get_current_admin),
):
    rows = (
        db.query(PayrollEmployee)
        .filter(PayrollEmployee.tenantid == current_admin.tenantid)
        .order_by(PayrollEmployee.empname)
        .all()
    )
    return [_to_response(row) for row in rows]


@router.get("/search", response_model=list[EmployeeResponse])
def search_employees(
    q: str,
    db: Session = Depends(get_db),
    current_admin: CurrentUser = Depends(get_current_admin),
):
    if not q or len(q.strip()) < 2:
        return []

    term = f"%{q.strip()}%"
    rows = (
        db.query(PayrollEmployee)
        .filter(
            PayrollEmployee.tenantid == current_admin.tenantid,
            or_(
                PayrollEmployee.empname.ilike(term),
                PayrollEmployee.email.ilike(term),
                PayrollEmployee.phoneno.ilike(term),
            ),
        )
        .order_by(PayrollEmployee.empname)
        .limit(20)
        .all()
    )
    return [_to_response(row) for row in rows]


@router.post("", response_model=EmployeeResponse)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_admin: CurrentUser = Depends(get_current_admin),
):
    """
    Creates a lightweight payroll `employee` row with just the fields this
    form collects. The real employee master record (payroll numbers, bank
    details, etc.) should still be filled in properly through the payroll
    system's own employee onboarding flow - this just lets a walk-in host be
    findable immediately.
    """
    existing = (
        db.query(PayrollEmployee)
        .filter(PayrollEmployee.email == payload.email, PayrollEmployee.tenantid == current_admin.tenantid)
        .first()
    )
    if existing:
        return _to_response(existing)

    empid = f"VMS-{uuid.uuid4().hex[:8].upper()}"
    employee = PayrollEmployee(
        empid=empid,
        tenantid=current_admin.tenantid,
        empname=payload.name,
        email=payload.email,
        phoneno=payload.phone,
        department=payload.department or "General",
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return _to_response(employee)
