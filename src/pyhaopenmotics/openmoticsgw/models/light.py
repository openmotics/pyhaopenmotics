"""Output Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .location import Location


@dataclass
class Status:

    """Class holding the status."""

    on: bool
    locked: bool
    manual_override: bool
    value: int

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
            # on = True if status = 1
            on=data.get("status") == 1,
            locked=data.get("locked", False),
            value=data.get("dimmer", 0),
            manual_override=data.get("manual_override", False),
        )


@dataclass
class Light:

    """Class holding an OpenMotics Light."""

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    location: Location
    capabilities: list[str]
    metadata: dict[str, Any]
    status: Status
    last_state_change: float
    version: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Light | None:
        """Return Output object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns
        -------
            A Output object.
        """
        status = Status.from_dict({})
        if "status" in data:
            status = Status.from_dict(data.get("status", {}))

        # Switch can always turn on/OFF
        capabilities = ["ON_OFF"]
        # Dimmmer
        if data.get("module_type") == "D":
            capabilities.append("RANGE")

        return Light(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            location=Location.from_dict(data),
            capabilities=capabilities,
            metadata={},
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
