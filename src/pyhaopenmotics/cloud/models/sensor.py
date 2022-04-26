"""Sensor Model for the OpenMotics API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .location import Location


class Status(BaseModel):
    """Class holding the status."""

    humidity: Optional[float]
    temperature: Optional[float]
    brightness: Optional[int]


class Sensor(BaseModel):
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
    idx: int = Field(..., alias="id")
    local_id: Optional[int]
    name: str
    location: Optional[Location]
    physical_quantity: Optional[str]
    status: Status
    last_state_change: Optional[float]
    version: Optional[str] = Field(..., alias="_version")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
