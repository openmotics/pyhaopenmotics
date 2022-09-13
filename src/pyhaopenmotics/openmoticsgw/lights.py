"""Module containing the base of an light."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .models.light import Light

if TYPE_CHECKING:
    from pyhaopenmotics.localgateway import LocalGateway  # pylint: disable=R0401


@dataclass
class OpenMoticsLights:  # noqa: SIM119
    """Object holding information of the OpenMotics lights.

    All actions related to lights or a specific light.
    """

    def __init__(self, omcloud: LocalGateway) -> None:
        """Init the installations object.

        Args:
            omcloud: LocalGateway
        """
        self._omcloud = omcloud

    async def get_all(  # noqa: A003
        self,
        light_filter: str | None = None,  # noqa: W0613
    ) -> list[Light]:
        """Get a list of all light objects.

        Args:
            light_filter: str

        Returns:
            list with all lights
        """

        return []
