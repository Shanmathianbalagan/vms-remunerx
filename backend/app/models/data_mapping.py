from sqlalchemy import Column, Integer, String
from app.database import Base


class DataMapping(Base):
    __tablename__ = "datamapping"

    datamappingid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenantid = Column(Integer, nullable=False, index=True)
    grouping = Column("grouping", String(200), nullable=False)
    description = Column(String(200), nullable=False)
    internalcode = Column(String(200), nullable=False)
    externalcode = Column(String(200), nullable=False)
    fieldvalue = Column(String(200), nullable=True)
