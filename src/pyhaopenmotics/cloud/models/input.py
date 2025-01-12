"""Output Model for the OpenMotics API."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class Status(DataClassORJSONMixin):
    """Class holding the status."""

    on: bool
    locked: bool | None = field(default=None)
    value: int | None = field(default=None)


@dataclass
class OMInput(DataClassORJSONMixin):
    """Class holding an OpenMotics Input.

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
    name: str
    idx: int = field(metadata=field_options(alias="id"))
    local_id: int | None = field(default=None)

    status: Status | None = field(default=None)
    last_state_change: float | None = field(default=None)
    room: int | None = field(default=None)
    version: str | None = field(
        default=None,
        metadata=field_options(alias="_version"),
    )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
