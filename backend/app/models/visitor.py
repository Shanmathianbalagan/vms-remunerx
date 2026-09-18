from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    visitor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenantid = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    photo_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    visits = relationship("Visit", back_populates="visitor")
