from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Badge(Base):
    __tablename__ = "badges"

    badge_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("visits.visit_id"), nullable=False)
    badge_code = Column(String(32), unique=True, nullable=False)
    status = Column(String(50), default="ISSUED")
    issued_at = Column(DateTime, server_default=func.now())

    visit = relationship("Visit", back_populates="badges")
