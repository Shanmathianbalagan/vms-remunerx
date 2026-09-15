from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    invitation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("visits.visit_id"), nullable=False)
    qr_code = Column(String(64), unique=True, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String(50), default="GENERATED")
    created_at = Column(DateTime, server_default=func.now())

    visit = relationship("Visit", back_populates="invitations")
