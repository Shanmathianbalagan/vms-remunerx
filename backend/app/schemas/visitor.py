from datetime import datetime
from pydantic import BaseModel


class VisitorCreate(BaseModel):
    name: str
    phone: str
    email: str | None = None
    company: str | None = None


class VisitorResponse(BaseModel):
    visitor_id: int
    name: str
    phone: str
    email: str | None = None
    company: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
