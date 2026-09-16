from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_employee
from app.models.employee import Employee
from app.schemas.checkin import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
)
from app.services.checkin_service import check_in, check_out

checkin_router = APIRouter(prefix="/api/checkin", tags=["checkin"])
checkout_router = APIRouter(prefix="/api/checkout", tags=["checkout"])


@checkin_router.post("", response_model=CheckInResponse)
def check_in_route(
    payload: CheckInRequest,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    visit, event, badge = check_in(db, payload.code, current_employee.employee_id)

    return CheckInResponse(
        visit_id=visit.visit_id,
        purpose=visit.purpose,
        visitor=visit.visitor,
        location=visit.location,
        checked_in_at=event.event_time,
        badge_code=badge.badge_code,
        badge_status=badge.status,
    )


@checkout_router.post("", response_model=CheckOutResponse)
def check_out_route(
    payload: CheckOutRequest,
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    visit, event, badge = check_out(db, payload.code, current_employee.employee_id)

    return CheckOutResponse(
        visit_id=visit.visit_id,
        purpose=visit.purpose,
        visitor=visit.visitor,
        location=visit.location,
        checked_out_at=event.event_time,
        badge_code=badge.badge_code,
        badge_status=badge.status,
    )
