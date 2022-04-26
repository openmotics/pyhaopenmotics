"""Groupaction Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .location import Location


@dataclass
class GroupAction:
    """Class holding an OpenMotics GroupAction.

    # noqa: E800
    # {
    # "_version": <version>,
    # "actions": [
    #     <action type>, <action number>,
    #     <action type>, <action number>,
    #     ...
    # ],
    # "id": <id>,
    # "location": {
    #     "installation_id": <installation id>
    # },
    # "name": "<name>"
    # }
    """

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    actions: list[Any]
    location: Location
    version: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> GroupAction | None:
        """Return GroupAction object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A GroupAction object.
        """
        actions = [""]

        return GroupAction(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            actions=actions,
            location=Location.from_dict(data),
            version=data.get("version", "0.0"),
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
