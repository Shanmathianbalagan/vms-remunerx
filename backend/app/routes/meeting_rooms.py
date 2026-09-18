from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser, get_current_user
from app.models.data_mapping import DataMapping
from app.schemas.meeting_room import MeetingRoomResponse

router = APIRouter(prefix="/api/meeting-rooms", tags=["meeting-rooms"])


@router.get("", response_model=list[MeetingRoomResponse])
def list_meeting_rooms(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    rows = (
        db.query(DataMapping)
        .filter(DataMapping.tenantid == current_user.tenantid, DataMapping.grouping == "MEETING ROOM")
        .order_by(DataMapping.internalcode)
        .all()
    )
    return [
        MeetingRoomResponse(meeting_room_id=row.datamappingid, name=row.internalcode)
        for row in rows
    ]
