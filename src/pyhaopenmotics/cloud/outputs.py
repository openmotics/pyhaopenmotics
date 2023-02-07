"""Module containing the base of an output."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import parse_obj_as

from pyhaopenmotics.cloud.models.output import Output

if TYPE_CHECKING:
    from pyhaopenmotics.openmoticscloud import OpenMoticsCloud  # pylint: disable=R0401


class OpenMoticsOutputs:  # noqa: SIM119

    """Object holding information of the OpenMotics outputs.

    All actions related to Outputs or a specific Output.
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
        output_filter: str | None = None,
    ) -> list[Output]:
        """Get a list of all output objects.

        Args:
            output_filter: str

        Returns
        -------
            A list of outputs
        """
        path = f"/base/installations/{self._omcloud.installation_id}/outputs"

        if output_filter:
            query_params = {"filter": output_filter}
            body = await self._omcloud.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self._omcloud.get(path)

        return parse_obj_as(list[Output], body["data"])

    async def get_by_id(
        self,
        output_id: int,
    ) -> Output:
        """Get output by id.

        Args:
            output_id: int

        Returns
        -------
            Returns a output with id
        """
        path = f"/base/installations/{self._omcloud.installation_id}/outputs/{output_id}"
        body = await self._omcloud.get(path)

        return Output.parse_obj(body["data"])

    async def toggle(
        self,
        output_id: int,
    ) -> Any:
        """Toggle a specified Output object.

        Args:
            output_id: int

        Returns
        -------
            Returns a output with id
        """
        path = f"/base/installations/{self._omcloud.installation_id}" f"/outputs/{output_id}/toggle"
        return await self._omcloud.post(path)

    async def turn_on(
        self,
        output_id: int,
        value: int | None = 100,
    ) -> Any:
        """Turn on a specified Output object.

        Args:
            output_id: int
            value: <0 - 100>

        Returns
        -------
            Returns a output with id
        """
        if value is not None:
            # value: <0 - 100>
            value = min(value, 100)
            value = max(0, value)

        path = (
            f"/base/installations/{self._omcloud.installation_id}" f"/outputs/{output_id}/turn_on"
        )
        payload = {"value": value}
        return await self._omcloud.post(path, json=payload)

    async def turn_off(
        self,
        output_id: int | None = None,
    ) -> Any:
        """Turn off a specified Output object.

        Args:
            output_id: int

        Returns
        -------
            Returns a output with id
        """
        if output_id is None:
            # Turn off all lights
            path = f"/base/installations/{self._omcloud.installation_id}" f"/outputs/turn_off"
        else:
            # Turn off light with id
            path = (
                f"/base/installations/{self._omcloud.installation_id}"
                f"/outputs/{output_id}/turn_off"
            )
        return await self._omcloud.post(path)
