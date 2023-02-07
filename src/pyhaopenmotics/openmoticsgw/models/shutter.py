"""Shutter Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .location import Location


@dataclass
class Status:

    """Class holding the status."""

    locked: bool
    manual_override: bool
    state: str
    position: int
    last_change: float
    preset_position: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Status:
        """Return Status object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns
        -------
            A Status object.
        """
        return Status(
            locked=data.get("locked", False),
            manual_override=data.get("manual_override", False),
            state=data.get("state", "None"),
            position=data.get("position", 0),
            last_change=data.get("last_change", 0),
            preset_position=data.get("preset_position", 0),
        )


@dataclass
class Attributes:

    """Class holding the Attributes."""

    azimuth: str
    compass_point: str
    surface_area: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Attributes:
        """Return Attributes object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns
        -------
            A Attributes object.
        """
        return Attributes(
            azimuth=data.get("azimuth", "None"),
            compass_point=data.get("compass_point", "None"),
            surface_area=data.get("surface_area", "None"),
        )


@dataclass
class Shutter:

    """Object holding an OpenMotics Shutter.

    # noqa: E800
    # {
    # "_version": <version>,
    # "configuration": {
    #     "group_1": null | <group id>,
    #     "group_2": null | <group id>,
    #     "name": "<name>",
    #     "steps": null | <number of steps>,
    #     "timer_down": <timer down>,
    #     "timer_up": <timer up>,
    #     "up_down_config": <up down configuration>
    # },
    # "id": <id>,
    # "capabilities": ["UP_DOWN", "POSITION", "RELATIVE_POSITION",
    #          "HW_LOCK"|"CLOUD_LOCK", "PRESET", "CHANGE_PRESET"],
    # "location": {
    #     "floor_coordinates": {
    #         "x": null | <x coordinate>,
    #         "y": null | <y coordinate>
    #     },
    #     "floor_id": null | <floor id>,
    #     "installation_id": <installation id>,
    #     "room_id": null | <room_id>
    # },
    # "name": "<name>",
    # "status": {
    #     "last_change": <epoch in seconds>
    #     "position": null | <position>,
    #     "state": null | "UP|DOWN|STOP|GOING_UP|GOING_DOWN",
    #     "locked": true | false,
    #     "manual_override": true | false
    # }
    # }
    """

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    shutter_type: str
    location: Location
    capabilities: list[str]
    attributes: Attributes
    metadata: dict[str, Any]
    status: Status
    version: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Shutter | None:
        """Return Shutter object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns
        -------
            A Shutter object.
        """
        status = Status.from_dict({})
        if "status" in data:
            status = Status.from_dict(data.get("status", {}))

        return Shutter(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            shutter_type=data.get("type", "None"),
            location=Location.from_dict(data),
            capabilities=data.get("capabilities", "None"),
            attributes=Attributes.from_dict(data),
            metadata={},
            status=status,
            version=data.get("version", "0.0"),
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
