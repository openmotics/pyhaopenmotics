"""Output Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .location import Location


@dataclass
class Status:

    """Class holding the status."""

    humidity: float
    temperature: float
    brightness: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Status:
        """Return Status object from OpenMotics API response.

        Args:
        ----
            data: The data from the OpenMotics API.

        Returns:
        -------
            A Status object.
        """
        return Status(
            # on = True if status = 1
            humidity=data.get("humidity", 0),
            temperature=data.get("temperature", 0),
            brightness=data.get("brightness", 0),
        )


@dataclass
class Sensor:

    """Class holding an OpenMotics Sensor.

    # noqa: E800
    #     {
    #     "_version": <version>,
    #     "id": <id>,
    #     "name": "<name>",
    #     "location": {
    #         "room_id": null | <room_id>,
    #         "installation_id": <installation id>
    #     },
    #     "status": {
    #         "humidity": null | <hunidity 0 - 100>,
    #         "temperature": null | <temperature -32 - 95>,
    #         "brightness": null | <brightness 0 - 100>
    #     }
    # }
     #     ...
    """

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    location: Location
    physical_quantity: str
    status: Status
    last_state_change: float
    version: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Sensor | None:
        """Return Output object from OpenMotics API response.

        Args:
        ----
            data: The data from the OpenMotics API.

        Returns:
        -------
            A Output object.
        """
        status = Status.from_dict({})
        if "status" in data:
            status = Status.from_dict(data.get("status", {}))

        return Sensor(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            location=Location.from_dict(data),
            physical_quantity=data.get("physical_quantity", "None"),
            status=status,
            last_state_change=data.get("last_state_change", None),
            version=data.get("version", "0.0"),
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
