from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), default="Headquarters")
    city = Column(String(100), default="Bangalore")
    created_at = Column(DateTime, server_default=func.now())

    visits = relationship("Visit", back_populates="location")
