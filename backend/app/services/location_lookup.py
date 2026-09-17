from sqlalchemy.orm import Session

from app.models.data_mapping import DataMapping
from app.models.location import Location
from app.models.meeting_room import MeetingRoom


def resolve_names(db: Session, grouping: str, legacy_model, ids: set[int | None]) -> dict[int, str]:
    """Resolve location/meeting-room ids to display names. Checks DATAMAPPING
    first; falls back to the legacy locations/meeting_rooms tables for the
    handful of visits created before that switch."""
    clean_ids = {i for i in ids if i is not None}
    if not clean_ids:
        return {}

    names: dict[int, str] = {
        row.datamappingid: row.internalcode
        for row in db.query(DataMapping).filter(
            DataMapping.grouping == grouping, DataMapping.datamappingid.in_(clean_ids)
        )
    }

    missing = clean_ids - names.keys()
    if missing:
        legacy_pk = "location_id" if legacy_model is Location else "meeting_room_id"
        for row in db.query(legacy_model).filter(getattr(legacy_model, legacy_pk).in_(missing)):
            names[getattr(row, legacy_pk)] = row.name

    return names
