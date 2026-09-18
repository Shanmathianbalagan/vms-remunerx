from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUser, get_current_user
from app.models.data_mapping import DataMapping
from app.schemas.location import LocationResponse

router = APIRouter(prefix="/api/locations", tags=["locations"])


@router.get("", response_model=list[LocationResponse])
def list_locations(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    rows = (
        db.query(DataMapping)
        .filter(DataMapping.tenantid == current_user.tenantid, DataMapping.grouping == "LOCATION")
        .order_by(DataMapping.internalcode)
        .all()
    )
    return [
        LocationResponse(location_id=row.datamappingid, name=row.internalcode)
        for row in rows
    ]
