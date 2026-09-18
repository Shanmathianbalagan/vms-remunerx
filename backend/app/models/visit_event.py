from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class VisitEvent(Base):
    __tablename__ = "visit_events"

    visit_event_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("visits.visit_id"), nullable=False)
    event_type = Column(String(20), nullable=False)  # CHECK_IN / CHECK_OUT
    event_time = Column(DateTime, server_default=func.now())
    recorded_by = Column(String(300), nullable=True)  # empid, or the admin's userid as text

    visit = relationship("Visit", back_populates="visit_events")
