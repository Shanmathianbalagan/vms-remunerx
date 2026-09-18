from sqlalchemy import Column, Integer, String
from app.database import Base


class PayrollEmployee(Base):
    """Maps onto the real payroll `employee` table (only the columns this app
    actually uses - the real table has many more payroll-specific fields)."""

    __tablename__ = "employee"

    msid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empid = Column(String(300), nullable=False, index=True)
    tenantid = Column(Integer, nullable=False, index=True)
    empname = Column(String(300), nullable=False)
    phoneno = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
