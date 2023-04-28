"""Output Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# from .location import Location


@dataclass
class Status:

    """Class holding the status."""

    on: bool
    locked: bool
    value: int

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
            on=data.get("status") == 1,
            locked=data.get("locked", False),
            value=data.get("dimmer", 0),
        )


@dataclass
class Input:

    """Class holding an OpenMotics Input.

    # noqa: E800
    # [{
    #     'name': 'name1',
    #     'type': 'OUTLET',
    #     'capabilities': ['ON_OFF'],
    #     'location': {'floor_coordinates': {'x': None, 'y': None},
    #          'installation_id': 21,
    #          'gateway_id': 408,
    #          'floor_id': None,
    #          'room_id': None},
    #     'metadata': None,
    #     'status': {'on': False, 'locked': False, 'manual_override': False},
    #     'last_state_change': 1633099611.275243,
    #     'id': 18,
    #     '_version': 1.0
    #     },{
    #     'name': 'name2',
    #     'type': 'OUTLET',
    #     ...
    """

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    status: Status
    last_state_change: float
    room: int 
    version: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Input | None:
        """Return Input object from OpenMotics API response.

        Args:
        ----
            data: The data from the OpenMotics API.

        Returns:
        -------
            A INput object.
        """
        status = Status.from_dict({})
        if "status" in data:
            status = Status.from_dict(data.get("status", {}))

        return Input(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            status=status,
            last_state_change=data.get("last_state_change", None),
            room=data.get("room", "None"),
            version=data.get("version", "0.0"),
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
