"""Output Model for the OpenMotics API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GroupLocation:
    """Class holding the location."""

    thermostat_group_id: int
    installation_id: int
    room_id: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> GroupLocation:
        """Return Status object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A GroupLocation object.
        """
        return GroupLocation(
            thermostat_group_id=data.get("thermostat_group_id", 0),
            installation_id=data.get("installation_id", 0),
            room_id=data.get("room_id", 0),
        )


@dataclass
class UnitLocation:
    """Class holding the location."""

    thermostat_group_id: int
    installation_id: int
    room_id: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UnitLocation:
        """Return Status object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A UnitLocation object.
        """
        return UnitLocation(
            thermostat_group_id=data.get("thermostat_group_id", 0),
            installation_id=data.get("installation_id", 0),
            room_id=data.get("room_id", 0),
        )


@dataclass
class GroupStatus:
    """Class holding the status."""

    mode: str
    state: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> GroupStatus:
        """Return GroupStatus object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A GroupStatus object.
        """
        return GroupStatus(
            mode=data.get("mode", "None"),
            state=data.get("state", False),
        )


@dataclass
class UnitStatus:
    """Class holding the status."""

    actual_temperature: float
    current_setpoint: float
    output_0: str
    output_1: str
    preset: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UnitStatus:
        """Return UnitStatus object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A UnitStatus object.
        """
        return UnitStatus(
            actual_temperature=data.get("actual_temperature", 0),
            current_setpoint=data.get("setpoint_temperature", 0),
            output_0=data.get("output_0", "None"),
            output_1=data.get("output_1", "None"),
            preset=data.get("preset", "None"),
        )


@dataclass
class Presets:
    """Class holding the status."""

    away: str
    party: str
    vacation: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Presets:
        """Return Presets object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Presets object.
        """
        return Presets(
            away=data.get("away", "None"),
            party=data.get("party", "None"),
            vacation=data.get("vacation", "None"),
        )


@dataclass
class Schedule:
    """Class holding the Schedule."""

    data: dict[str, Any]
    start: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Schedule:
        """Return Schedule object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Schedule object.
        """
        return Schedule(
            data=data.get("data", "None"),
            start=data.get("start", "None"),
        )


@dataclass
class ConfigurationPreset:
    """Class holding the ConfigurationPreset."""

    output_0_id: int
    output_1_id: int
    presets: Presets
    schedule: Schedule
    sensor_id: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ConfigurationPreset:
        """Return ConfigurationPreset object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A ConfigurationPreset object.
        """
        return ConfigurationPreset(
            output_0_id=data.get("output_0_id", 0),
            output_1_id=data.get("output_1_id", 0),
            presets=Presets.from_dict(data),
            schedule=Schedule.from_dict(data),
            sensor_id=data.get("sensor_id", 0),
        )


@dataclass
class Allowed:
    """Class holding the Configuration."""

    allowed: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Allowed:
        """Return Allowed object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Allowed object.
        """
        return Allowed(
            allowed=data.get("allowed", False),
        )


@dataclass
class Acl:
    """Class holding the Acl."""

    set_state: Allowed
    set_mode: Allowed

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Acl:
        """Return Acl object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Acl object.
        """
        return Acl(
            set_state=Allowed.from_dict(data),
            set_mode=Allowed.from_dict(data),
        )


@dataclass
class Configuration:
    """Class holding the Configuration."""

    heating: ConfigurationPreset
    cooling: ConfigurationPreset

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Configuration:
        """Return Configuration object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A Configuration object.
        """
        return Configuration(
            heating=ConfigurationPreset.from_dict(data),
            cooling=ConfigurationPreset.from_dict(data),
        )


@dataclass
class ThermostatGroup:
    """Class holding an OpenMotics ThermostatGroup."""

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    schedule: Schedule
    capabilities: list[Any]
    version: str
    thermostat_ids: dict[str, Any]
    status: GroupStatus
    acl: Acl

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ThermostatGroup | None:
        """Return ThermostatGroup object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A ThermostatGroup object.
        """

        status = GroupStatus.from_dict({})
        if "status" in data:
            status = GroupStatus.from_dict(data.get("status", {}))

        # placeholders
        capabilities = ["None"]
        thermostat_ids = {"ids": "None"}

        return ThermostatGroup(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            schedule=Schedule.from_dict(data),
            capabilities=capabilities,
            version=data.get("version", "0.0"),
            thermostat_ids=thermostat_ids,
            acl=Acl.from_dict(data),
            status=status,
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"


@dataclass
class ThermostatUnit:
    """Class holding an OpenMotics ThermostatUnit."""

    # pylint: disable=too-many-instance-attributes
    idx: int
    local_id: int
    name: str
    location: UnitLocation
    status: UnitStatus
    version: str
    acl: Acl

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ThermostatUnit | None:
        """Return ThermostatUnit object from OpenMotics API response.

        Args:
            data: The data from the OpenMotics API.

        Returns:
            A ThermostatUnit object.
        """

        status = UnitStatus.from_dict({})
        if "status" in data:
            status = UnitStatus.from_dict(data.get("status", {}))

        return ThermostatUnit(
            idx=data.get("id", 0),
            local_id=data.get("id", 0),
            name=data.get("name", "None"),
            location=UnitLocation.from_dict(data),
            version=data.get("version", "0.0"),
            acl=Acl.from_dict(data),
            status=status,
        )

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
