"""Module containing the base of an light."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pyhaopenmotics.helpers import merge_dicts

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
        self._light_configs: list[Any] = []

    @property
    def light_configs(self) -> list[Any]:
        """Get a list of all output confs.

        Returns:
            list of all output confs
        """
        return self._light_configs

    @light_configs.setter
    def light_configs(self, light_configs: list[Any]) -> None:
        """Set a list of all output confs.

        Args:
            light_configs: list
        """
        self._light_configs = light_configs

    async def get_all(  # noqa: A003
        self,
        light_filter: str | None = None,
    ) -> list[Light]:
        """Get a list of all light objects.

        Args:
            light_filter: str

        Returns:
            list with all lights
        """

        if len(self.light_configs) == 0:
            goc = await self._omcloud.exec_action("get_light_configurations")
            if goc["success"] is True:
                self.light_configs = goc["config"]

        light_status = await self._omcloud.exec_action("get_light_status")
        status = light_status["status"]

        data = merge_dicts(self.light_configs, "status", status)

        lights = [Light.from_dict(device) for device in data]

        if light_filter is not None:
            # implemented later
            pass

        return lights  # type: ignore
