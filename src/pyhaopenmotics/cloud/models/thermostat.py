"""Thermostat Model for the OpenMotics API."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class GroupLocation(BaseModel):
    """Class holding the location."""

    thermostat_group_id: Optional[int]
    installation_id: Optional[int]
    room_id: Optional[int]


class UnitLocation(BaseModel):
    """Class holding the location."""

    thermostat_group_id: Optional[int]
    installation_id: Optional[int]
    room_id: Optional[int]


class GroupStatus(BaseModel):
    """Class holding the status."""

    mode: Optional[str]
    state: Optional[bool]


class UnitStatus(BaseModel):
    """Class holding the status."""

    actual_temperature: Optional[float]
    current_setpoint: Optional[float]
    output_0: Optional[str]
    output_1: Optional[str]
    preset: Optional[str]


class Presets(BaseModel):
    """Class holding the status."""

    away: Optional[str]
    party: Optional[str]
    vacation: Optional[str]


class Schedule(BaseModel):
    """Class holding the schedule."""

    data: Optional[dict[str, Any]]
    start: Optional[str]


class ConfigurationPreset(BaseModel):
    """Class holding the configuration presets."""

    output_0_id: Optional[int]
    output_1_id: Optional[int]
    presets: Optional[Presets]
    schedule: Optional[Schedule]
    sensor_id: Optional[int]


class Configuration(BaseModel):
    """Class holding the configuration."""

    heating: Optional[ConfigurationPreset]
    cooling: Optional[ConfigurationPreset]


class Allowed(BaseModel):
    """Object holding allowed."""

    allowed: Optional[bool]


class Acl(BaseModel):
    """Object holding an acl."""

    set_state: Optional[Allowed]
    set_mode: Optional[Allowed]


class ThermostatGroup(BaseModel):
    """Class holding an OpenMotics ThermostatGroup .

        # noqa: E800
    #  {
    #     "_acl": <acl>,
    #     "_version": <version>,
    #     "schedule": {
    #         "<optional timestamp>": "AUTO|AWAY|PARTY|VACATION",
    #         ...
    #     },
    #     "status": {
    #         "mode": "HEATING|COOLING",
    #         "state": "ON|OFF"
    #     },
    #     "capabilities": ["HEATING", "COOLING"]
    # }

    """

    # pylint: disable=too-many-instance-attributes
    idx: int = Field(..., alias="id")
    local_id: int
    name: str
    schedule: Optional[Schedule]
    capabilities: Optional[list[Any]]
    version: Optional[str] = Field(..., alias="_version")
    thermostat_ids: Optional[dict[str, Any]]
    status: Optional[GroupStatus]
    acl: Optional[Acl] = Field(..., alias="_acl")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"


class ThermostatUnit(BaseModel):
    """Class holding an OpenMotics ThermostatUnit.

    # noqa: E800
    # {
    #     "_version": <version>,
    #     "configuration": {
    #         "heating": {
    #             "output_0_id": <first output id>,
    #             "output_1_id": null | <second output id>,
    #             "presets": {`
    #                 "AWAY": <away temperature>,
    #                 "PARTY": <party temperature>,
    #                 "VACATION": <vacation temperature>
    #             },
    #             "schedule": {
    #                 "data": [
    #                     {
    #                         "0": <temperature from this timestamp>,
    #                         "23400": <temperature from this timestamp>,
    #                         "30600": <temperature from this timestamp>,
    #                         "61200": <temperature from this timestamp>,
    #                         "84600": <temperature from this timestamp>
    #                     },
    #                     ...
    #                 ],
    #                 "start": <timestamp on which schedule needs to be based>
    #             },
    #             "sensor_id": <room sensor id>
    #         },
    #         "cooling": {
    #             "output_0_id": <first output id>,
    #             "output_1_id": null | <second output id>,
    #             "presets": {
    #                 "AWAY": <away temperature>,
    #                 "PARTY": <party temperature>,
    #                 "VACATION": <vacation temperature>
    #             },
    #             "schedule": {
    #                 "data": [
    #                     {
    #                         "0": <temperature from this timestamp>,
    #                         "23400": <temperature from this timestamp>,
    #                         "30600": <temperature from this timestamp>,
    #                         "61200": <temperature from this timestamp>,
    #                         "84600": <temperature from this timestamp>
    #                     },
    #                     ...
    #                 ],
    #                 "start": <timestamp on which schedule needs to be based>
    #             },
    #             "sensor_id": <room sensor id>
    #         }
    #     },
    #     "id": <id>,
    #     "location": {
    #         "installation_id": <installation id>,
    #         "room_id": null | <room id>,
    #         "thermostat_group_id": <thermostat group id>
    #     },
    #     "name": "<name>",
    #     "status": {
    #         "actual_temperature": <current measured temperature>,
    #         "current_setpoint": <desired temperature>,
    #         "output_0": <level of first output>,
    #         "output_1": <level of second output>,
    #         "preset": "AUTO|PARTY|AWAY|VACATION"
    #     }
    # }
    """

    # pylint: disable=too-many-instance-attributes
    idx: int = Field(..., alias="id")
    local_id: Optional[int]
    name: str
    location: Optional[UnitLocation] = None
    status: Optional[UnitStatus]
    version: Optional[str] = Field(..., alias="_version")
    acl: Optional[str] = Field(..., alias="_acl")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
