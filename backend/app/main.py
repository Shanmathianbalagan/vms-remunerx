from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import employee, location, user, visitor, visit, invitation, notification, approval, visit_event, badge  # noqa: F401 (ensures tables are registered)
from app.routes import auth, visits, visitors, locations, approvals, checkin

Base.metadata.create_all(bind=engine)

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
app.include_router(approvals.router)
app.include_router(checkin.checkin_router)
app.include_router(checkin.checkout_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
