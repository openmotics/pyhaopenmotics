"""Module containing the base of an sensor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import parse_obj_as

from pyhaopenmotics.cloud.models.sensor import Sensor

if TYPE_CHECKING:
    from pyhaopenmotics.openmoticscloud import OpenMoticsCloud  # pylint: disable=R0401


class OpenMoticsSensors:  # noqa: SIM119

    """Object holding information of the OpenMotics sensors.

    All actions related to Sensors or a specific Sensor.
    """

    def __init__(self, omcloud: OpenMoticsCloud) -> None:
        """Init the installations object.

        Args:
        ----
            omcloud: OpenMoticsCloud
        """
        self._omcloud = omcloud

    async def get_all(  # noqa: A003
        self,
        sensor_filter: str | None = None,
    ) -> list[Sensor]:
        """Get a list of all sensor objects.

        Args:
        ----
            sensor_filter: str

        Returns:
        -------
            Dict with all sensors
        """
        path = f"/base/installations/{self._omcloud.installation_id}/sensors"

        if sensor_filter:
            query_params = {"filter": sensor_filter}
            body = await self._omcloud.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self._omcloud.get(path)

        return parse_obj_as(list[Sensor], body["data"])

    async def get_by_id(
        self,
        sensor_id: int,
    ) -> Sensor:
        """Get sensor by id.

        Args:
        ----
            sensor_id: int

        Returns:
        -------
            Returns a sensor with id
        """
        path = f"/base/installations/{self._omcloud.installation_id}/sensors/{sensor_id}"
        body = await self._omcloud.get(path)

        return Sensor.parse_obj(body["data"])
