"""Location Model for the OpenMotics API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class FloorCoordinates(DataClassORJSONMixin):
    """Class holding the floor_coordinates."""

    x: int | None = field(default=None)
    y: int | None = field(default=None)


@dataclass
class Location(DataClassORJSONMixin):
    """Class holding the location."""

    floor_coordinates: FloorCoordinates | None = field(default=None)
    installation_id: int | None = field(default=None)
    gateway_id: int | None = field(default=None)
    floor_id: int | None = field(default=None)
    room_id: int | None = field(default=None)
