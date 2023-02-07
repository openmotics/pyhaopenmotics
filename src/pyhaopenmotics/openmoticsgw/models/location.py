"""Location Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FloorCoordinates:

    """Class holding the floor_coordinates."""

    x: int  # pylint: disable-msg=C0103
    y: int  # pylint: disable-msg=C0103

    @staticmethod
    def from_dict(data: dict[str, Any]) -> FloorCoordinates | None:
        """Get floor coordinates from data.

        Args:
            data: dict

        Returns
        -------
            FloorCoordinates object
        """
        if "x" not in data or "y" not in data:
            return None

        return FloorCoordinates(
            x=data.get("x", 0),
            y=data.get("y", 0),
        )


@dataclass
class Location:

    """Class holding the location."""

    floor_coordinates: FloorCoordinates | None
    installation_id: int
    gateway_id: int
    floor_id: int
    room_id: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Location:
        """Get location coordinates from data.

        Args:
            data: dict

        Returns
        -------
            Location object
        """
        _floor_coordinates: FloorCoordinates | None
        _room_id: int

        if data is not None:
            if "room_id" in data:
                _room_id = data.get("room_id", 0)
            else:
                _room_id = data.get("room", 0)

            if "floor_coordinates" in data:
                _floor_coordinates = FloorCoordinates.from_dict(data.get("floor_coordinates", {}))
            else:
                _floor_coordinates = None

        return Location(
            floor_coordinates=_floor_coordinates,
            installation_id=data.get("installation_id", 0),
            gateway_id=data.get("gateway_id", 0),
            floor_id=data.get("floor_id", 0),
            room_id=_room_id,
        )
