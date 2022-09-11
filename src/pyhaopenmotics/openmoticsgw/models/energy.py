"""Output Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Status:
    """Class holding the status."""

    voltage: float
    frequency: float
    current: float
    power: float

    @staticmethod
    def from_list(data: list[float]) -> Status:
        """Return Status object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Status object.
        """
        return Status(
            voltage=data[0] if len(data) > 0 else 0,
            frequency=data[1] if len(data) > 1 else 0,
            current=data[2] if len(data) > 2 else 0,
            power=data[3] if len(data) > 3 else 0,
        )


@dataclass
class EnergySensor:
    """Class holding an OpenMotics Energy Sensor.

    # noqa: E800
    #     {
    #     "id": <id>,
    #     "name": "<name>",
    #     "status": [
    #         <voltage>,
    #         <frequency>,
    #         <current>,
    #         <power>
    #     ],
    #     "inverted: <inverted>
    # }
    #     ...
    """

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    status: Status
    inverted: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> EnergySensor | None:
        """Return EnergySensor object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A EnergySensor object.
        """

        status = Status.from_list([])
        if "status" in data:
            status = Status.from_list(data.get("status", []))

        return EnergySensor(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            status=status,
            inverted=data.get("inverted", False),
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
