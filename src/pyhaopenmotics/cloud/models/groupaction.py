"""Groupaction Model for the OpenMotics API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .location import Location


class GroupAction(BaseModel):
    """Object holding an OpenMotics GroupAction.

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

    idx: int = Field(..., alias="id")
    local_id: int | None = None
    name: str | None = None
    actions: list[Any] | None = None
    location: Location | None = None
    version: str | None = Field(None, alias="_version")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
