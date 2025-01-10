"""Thermostat Model for the OpenMotics API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GroupLocation(BaseModel):
    """Class holding the location."""

    thermostat_group_id: int | None = None
    installation_id: int | None = None
    room_id: int | None = None


class UnitLocation(BaseModel):
    """Class holding the location."""

    thermostat_group_id: int | None = None
    installation_id: int | None = None
    room_id: int | None = None


class GroupStatus(BaseModel):
    """Class holding the status."""

    mode: str | None = None
    state: bool | None = None


class UnitStatus(BaseModel):
    """Class holding the status."""

    state: str | None = None
    setpoint: float | None = None
    steering_power: float | None = None
    active_preset: str | None = None
    current_temperature: float | None = None
    mode: str | None = None
    preset_expiration: str | None = None
    actual_temperature: float | None = None
    current_setpoint: float | None = None
    preset: str | None = None


class Presets(BaseModel):
    """Class holding the status."""

    away: str | None = None
    party: str | None = None
    vacation: str | None = None


class Schedule(BaseModel):
    """Class holding the schedule."""

    data: dict[str, Any] | None = None
    start: str | None = None


class ConfigurationPreset(BaseModel):
    """Class holding the configuration presets."""

    output_0_id: int | None = None
    output_1_id: int | None = None
    presets: Presets | None = None
    schedule: Schedule | None = None
    sensor_id: int | None = None


class Configuration(BaseModel):
    """Class holding the configuration."""

    heating: ConfigurationPreset | None = None
    cooling: ConfigurationPreset | None = None


class Allowed(BaseModel):
    """Object holding allowed."""

    allowed: bool | None = None


class Acl(BaseModel):
    """Object holding an acl."""

    set_state: Allowed | None = None
    set_mode: Allowed | None = None


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
    schedule: Schedule | None = None
    capabilities: list[Any] | None = None
    version: str | None = Field(..., alias="_version")
    thermostat_ids: list[Any] | None = None
    status: GroupStatus | None = None
    acl: Acl | None = Field(..., alias="_acl")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
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
    #           "state":"ON",
    #           "setpoint":13.0,
    #           "steering_power":0,
    #           "active_preset":"AUTO",
    #           "current_temperature":18.5,
    #           "mode":"HEATING",
    #           "preset_expiration":null,
    #           "actual_temperature":18.5,
    #           "current_setpoint":13.0,
    #           "preset":"AUTO"},
    # #     }
    # }
    """

    # pylint: disable=too-many-instance-attributes
    idx: int = Field(..., alias="id")
    local_id: int | None = None
    name: str
    location: UnitLocation | None = None
    status: UnitStatus | None = None
    version: str | None = Field(..., alias="_version")

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
