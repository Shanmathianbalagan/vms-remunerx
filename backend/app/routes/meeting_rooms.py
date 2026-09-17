from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_employee
from app.models.data_mapping import DataMapping
from app.models.employee import Employee
from app.schemas.meeting_room import MeetingRoomResponse

router = APIRouter(prefix="/api/meeting-rooms", tags=["meeting-rooms"])

# TODO: no real per-tenant session context exists yet - hardcoded to match the
# seeded DATAMAPPING tenant until proper multi-tenant login is wired up.
DEFAULT_TENANT_ID = 24


@router.get("", response_model=list[MeetingRoomResponse])
def list_meeting_rooms(
    db: Session = Depends(get_db),
    current_employee: Employee = Depends(get_current_employee),
):
    rows = (
        db.query(DataMapping)
        .filter(DataMapping.tenantid == DEFAULT_TENANT_ID, DataMapping.grouping == "MEETING ROOM")
        .order_by(DataMapping.internalcode)
        .all()
    )
    return [
        MeetingRoomResponse(meeting_room_id=row.datamappingid, name=row.internalcode)
        for row in rows
    ]
