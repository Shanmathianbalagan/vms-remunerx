from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    department: str | None = None


class EmployeeResponse(BaseModel):
    employee_id: str  # this is the empid (text), field name kept for API compatibility
    name: str
    email: str | None = None
    department: str | None = None
    phone: str | None = None
