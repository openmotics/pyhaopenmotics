"""Light Model for the OpenMotics API."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from .location import Location


class Status(BaseModel):
    """Class holding the status."""

    on: bool
    locked: bool | None
    manual_override: bool | None
    value: int | None


class Light(BaseModel):
    """Class holding an OpenMotics Light.

    # noqa: E800
    #      # {
    #     "_version": <version>,
    #     "capabilities": [
    #         "ON_OFF|RANGE|WHITE_TEMP|FULL_COLOR"
    #     ],
    #     "id": <id>,
    #     "location": {
    #         "floor_coordinates": {
    #             "x": <x coordinate>,
    #             "y": <y coordinate>
    #         },
    #         "floor_id": <floor id>,
    #         "installation_id": <installation id>,
    #         "room_id": <room id>
    #     },
    #     "name": "<name>",
    #     "status": {
    #         "on": true|false
    #     },
    # }
     #     ...
    """

    # pylint: disable=too-many-instance-attributes
    idx: int = Field(..., alias="id")
    local_id: int | None
    name: str | None
    capabilities: list[Any] | None
    location: Location | None
    status: Status | None
    version: Optional[str] = Field(None, alias="_version")

    _brightness: int | None

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
