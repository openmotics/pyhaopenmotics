"""Location Model for the OpenMotics API."""

from __future__ import annotations

from pydantic import BaseModel


class FloorCoordinates(BaseModel):
    """Class holding the floor_coordinates."""

    x: int | None = None
    y: int | None = None


class Location(BaseModel):
    """Class holding the location."""

    floor_coordinates: FloorCoordinates | None = None
    installation_id: int | None = None
    gateway_id: int | None = None
    floor_id: int | None = None
    room_id: int | None = None
