from pydantic import BaseModel


class LocationResponse(BaseModel):
    location_id: int
    name: str
    address: str | None = None
    city: str | None = None

    class Config:
        from_attributes = True
