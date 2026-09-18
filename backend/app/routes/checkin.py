from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser, get_current_user
from app.schemas.checkin import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
)
from app.services.checkin_service import check_in, check_out

checkin_router = APIRouter(prefix="/api/checkin", tags=["checkin"])
checkout_router = APIRouter(prefix="/api/checkout", tags=["checkout"])


def _actor_identifier(current_user: CurrentUser) -> str:
    # Whoever is operating the check-in desk - an employee's own empid, or the
    # admin/security account's userid if there's no empid (admin accounts).
    return current_user.empid or current_user.sub


@checkin_router.post("", response_model=CheckInResponse)
def check_in_route(
    payload: CheckInRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    visit, event, badge = check_in(db, payload.code, _actor_identifier(current_user))

    return CheckInResponse(
        visit_id=visit.visit_id,
        purpose=visit.purpose,
        visitor=visit.visitor,
        location={"name": visit.locations},
        checked_in_at=event.event_time,
        badge_code=badge.badge_code,
        badge_status=badge.status,
    )


@checkout_router.post("", response_model=CheckOutResponse)
def check_out_route(
    payload: CheckOutRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    visit, event, badge = check_out(db, payload.code, _actor_identifier(current_user))

    return CheckOutResponse(
        visit_id=visit.visit_id,
        purpose=visit.purpose,
        visitor=visit.visitor,
        location={"name": visit.locations},
        checked_out_at=event.event_time,
        badge_code=badge.badge_code,
        badge_status=badge.status,
    )
