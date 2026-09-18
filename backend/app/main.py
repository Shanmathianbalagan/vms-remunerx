from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import data_mapping, payroll_employee, visitor, visit, invitation, notification, approval, visit_event, badge  # noqa: F401 (ensures tables are registered)
from app.routes import auth, visits, visitors, locations, meeting_rooms, approvals, checkin, employees

# vw_login_users is a real database VIEW, not a table we own - creating it here
# would fail (or worse, shadow the payroll team's real view), so it's excluded
# from create_all even though PayrollLoginUser is mapped onto it for querying.
# payroll_employee (`employee`) and data_mapping (`datamapping`) also already
# exist as real tables - create_all skips them automatically since they're
# already present.
_tables_to_create = [t for name, t in Base.metadata.tables.items() if name != "vw_login_users"]
Base.metadata.create_all(bind=engine, tables=_tables_to_create)

app = FastAPI(title="VMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(visits.router)
app.include_router(visitors.router)
app.include_router(locations.router)
app.include_router(meeting_rooms.router)
app.include_router(approvals.router)
app.include_router(checkin.checkin_router)
app.include_router(checkin.checkout_router)
app.include_router(employees.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
