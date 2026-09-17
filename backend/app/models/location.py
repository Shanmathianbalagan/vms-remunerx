from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

# Legacy - superseded by DATAMAPPING (grouping='LOCATION'). Kept only because
# a couple of early test visits still reference rows here.
class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(Integer, nullable=False, default=1, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), default="Headquarters")
    city = Column(String(100), default="Bangalore")
    created_at = Column(DateTime, server_default=func.now())
