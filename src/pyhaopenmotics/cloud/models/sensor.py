"""Sensor Model for the OpenMotics API."""
from __future__ import annotations

from pydantic import BaseModel, Field, validator

from .location import Location

zombie_status = {
        "humidity" : None,
        "temperature": None,
        "brightness": None
        }

class Status(BaseModel):

    """Class holding the status."""

    humidity: float | None
    temperature: float | None
    brightness: int | None


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
    local_id: int | None
    name: str
    location: Location | None
    physical_quantity: str | None
    status: Status
    last_state_change: float | None
    version: str | None = Field(..., alias="_version")

    @validator("status", pre=True)
    def replace_none(cls, v):
        return v or zombie_status

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
