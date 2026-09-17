from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

# Legacy - superseded by DATAMAPPING (grouping='MEETING ROOM'). Kept only
# because a couple of early test visits still reference rows here.
class MeetingRoom(Base):
    __tablename__ = "meeting_rooms"

    meeting_room_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(Integer, nullable=False, default=1, index=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
