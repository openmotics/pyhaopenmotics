"""Location Model for the OpenMotics API."""
from __future__ import annotations

from pydantic import BaseModel


class FloorCoordinates(BaseModel):

    """Class holding the floor_coordinates."""

    x: int | None
    y: int | None


class Location(BaseModel):

    """Class holding the location."""

    floor_coordinates: FloorCoordinates | None
    installation_id: int | None
    gateway_id: int | None
    floor_id: int | None
    room_id: int | None
