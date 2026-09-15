from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="EMPLOYEE")
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="user")
