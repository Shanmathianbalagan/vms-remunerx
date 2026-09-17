from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    approval_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(Integer, nullable=False, default=1, index=True)
    visit_id = Column(Integer, ForeignKey("visits.visit_id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    status = Column(String(50), default="PENDING")
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    decided_at = Column(DateTime, nullable=True)

    visit = relationship("Visit", back_populates="approvals")
    approver = relationship("Employee")
