from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    department: str | None = None


class EmployeeResponse(BaseModel):
    employee_id: int
    name: str
    email: str
    department: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True
