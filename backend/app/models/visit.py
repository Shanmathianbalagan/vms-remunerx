from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visitor_id = Column(Integer, ForeignKey("visitors.visitor_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    purpose = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(50), default="CREATED")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    visitor = relationship("Visitor", back_populates="visits")
    employee = relationship("Employee", back_populates="visits")
    location = relationship("Location", back_populates="visits")
    invitations = relationship("Invitation", back_populates="visit")
    notifications = relationship("Notification", back_populates="visit")
    approvals = relationship("Approval", back_populates="visit")
    visit_events = relationship("VisitEvent", back_populates="visit")
    badges = relationship("Badge", back_populates="visit")
