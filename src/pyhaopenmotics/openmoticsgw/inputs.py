"""Module containing the base of an output."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pyhaopenmotics.helpers import merge_dicts

from .models.input import Input

if TYPE_CHECKING:
    from pyhaopenmotics.localgateway import LocalGateway  # pylint: disable=R0401


@dataclass
class OpenMoticsInputs:

    """Object holding information of the OpenMotics outputs.

    All actions related to Outputs or a specific Output.
    """

    def __init__(self, omcloud: LocalGateway) -> None:
        """Init the installations object.

        Args:
        ----
            omcloud: LocalGateway
        """
        self._omcloud = omcloud
        self._input_configs: list[Any] = []

    @property
    def input_configs(self) -> list[Any]:
        """Get a list of all input confs.

        Returns
        -------
            list of all input confs
        """
        return self._input_configs

    @input_configs.setter
    def input_configs(self, input_configs: list[Any]) -> None:
        """Set a list of all input confs.

        Args:
        ----
            input_configs: list
        """
        self._input_configs = input_configs

    async def get_all(
        self,
        input_filter: str | None = None,
    ) -> list[Input]:
        """Get a list of all input objects.

        Args:
        ----
            input_filter: str

        Returns:
        -------
            list with all inputs
        """
        if len(self.input_configs) == 0:
            goc = await self._omcloud.exec_action("get_input_configurations")
            if goc["success"] is True:
                self.input_configs = goc["config"]

        inputs_status = await self._omcloud.exec_action("get_input_status")
        status = inputs_status["status"]

        data = merge_dicts(self.input_configs, "status", status)

        if input_filter is not None:
            # implemented later
            pass

        inputs = [Input.from_dict(device) for device in data]

        return inputs  # type: ignore

    async def get_by_id(
        self,
        input_id: int,
    ) -> Input | None:
        """Get input by id.

        Args:
        ----
            input_id: int

        Returns:
        -------
            Returns a input with id
        """
        for input in await self.get_all():
            if input.idx == input_id:
                return input
        return None