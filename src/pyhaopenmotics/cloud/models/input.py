"""Output Model for the OpenMotics API."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Status(BaseModel):

    """Class holding the status."""

    on: bool
    locked: bool | None
    value: int | None


class Input(BaseModel):

    """Class holding an OpenMotics Output.

    # noqa: E800
     # [{
     #     'name': 'name1',
     #     'type': 'OUTLET|LIGHT',
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
    idx: int = Field(..., alias="id")
    local_id: int | None
    name: str
    status: Status | None
    last_state_change: float | None
    room: int | None
    version: str = Field(..., alias="_version")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}_{self.input_type}"
