from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(Integer, nullable=False, default=1, index=True)
    visit_id = Column(Integer, ForeignKey("visits.visit_id"), nullable=False)
    type = Column(String(50), nullable=False)
    channel = Column(String(20), default="EMAIL")
    recipient = Column(String(100), nullable=True)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, server_default=func.now())
    sent_at = Column(DateTime, nullable=True)

    visit = relationship("Visit", back_populates="notifications")
