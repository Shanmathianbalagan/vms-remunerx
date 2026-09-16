from datetime import datetime
from pydantic import BaseModel

from app.schemas.visit import LocationSummary, VisitorSummary


class CheckInRequest(BaseModel):
    code: str


class CheckInResponse(BaseModel):
    visit_id: int
    purpose: str
    visitor: VisitorSummary
    location: LocationSummary
    checked_in_at: datetime
    badge_code: str
    badge_status: str


class CheckOutRequest(BaseModel):
    code: str


class CheckOutResponse(BaseModel):
    visit_id: int
    purpose: str
    visitor: VisitorSummary
    location: LocationSummary
    checked_out_at: datetime
    badge_code: str
    badge_status: str
