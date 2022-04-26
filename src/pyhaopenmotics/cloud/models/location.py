"""Location Model for the OpenMotics API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class FloorCoordinates(BaseModel):
    """Class holding the floor_coordinates."""

    x: Optional[int] = None
    y: Optional[int] = None


class Location(BaseModel):
    """Class holding the location."""

    floor_coordinates: Optional[FloorCoordinates] = None
    installation_id: Optional[int] = None
    gateway_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None
