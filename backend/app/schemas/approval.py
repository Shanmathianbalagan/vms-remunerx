from datetime import date, time, datetime
from pydantic import BaseModel, field_validator

from app.schemas.visit import LocationSummary, VisitorSummary


class ApprovalVisitSummary(BaseModel):
    visit_id: int
    purpose: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    status: str
    visitor: VisitorSummary
    location: LocationSummary

    class Config:
        from_attributes = True


class ApprovalResponse(BaseModel):
    approval_id: int
    status: str
    comments: str | None = None
    created_at: datetime
    decided_at: datetime | None = None
    visit: ApprovalVisitSummary

    class Config:
        from_attributes = True


class ApprovalDecision(BaseModel):
    status: str
    comments: str | None = None

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, v: str) -> str:
        if v not in ("APPROVED", "REJECTED"):
            raise ValueError("Status must be APPROVED or REJECTED")
        return v
