from pydantic import BaseModel


class MeetingRoomResponse(BaseModel):
    meeting_room_id: int
    name: str
    capacity: int | None = None

    class Config:
        from_attributes = True
