from datetime import date, time, datetime
from pydantic import BaseModel, field_validator, model_validator


class VisitCreate(BaseModel):
    visitor_id: int
    location_id: int  # a DATAMAPPING id (grouping='LOCATION') - resolved to text at save time
    meeting_room_id: int | None = None  # a DATAMAPPING id (grouping='MEETING ROOM')
    purpose: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    notes: str | None = None
    host_employee_id: str | None = None  # admin-only: host on behalf of this empid

    @field_validator("purpose")
    @classmethod
    def purpose_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Purpose is required")
        return v.strip()

    @model_validator(mode="after")
    def check_dates_and_times(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be on or before end date")
        if self.start_date == self.end_date and self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")
        return self


class VisitorSummary(BaseModel):
    visitor_id: int
    name: str
    company: str | None = None

    class Config:
        from_attributes = True


class LocationSummary(BaseModel):
    name: str


class MeetingRoomSummary(BaseModel):
    name: str


class HostSummary(BaseModel):
    employee_id: str  # this is the empid (text), field name kept for API compatibility
    name: str


class VisitResponse(BaseModel):
    visit_id: int
    purpose: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    status: str
    notes: str | None = None
    created_at: datetime
    visitor: VisitorSummary
    location: LocationSummary
    meeting_room: MeetingRoomSummary | None = None
    employee: HostSummary

    class Config:
        from_attributes = True
