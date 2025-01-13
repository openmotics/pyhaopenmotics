"""Installation Model for the OpenMotics API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class Allowed(DataClassORJSONMixin):
    """Object holding an OpenMotics Installation."""

    allowed: bool | None = field(default=None)


@dataclass
class Acl(DataClassORJSONMixin):
    """Object holding an OpenMotics Installation."""

    configure: Allowed | None = field(default=None)
    view: Allowed | None = field(default=None)
    control: Allowed | None = field(default=None)


@dataclass
class Network(DataClassORJSONMixin):
    """Object holding an OpenMotics Installation."""

    local_ip_address: str | None = field(default=None)


@dataclass
class Installation(DataClassORJSONMixin):
    """Object holding an OpenMotics Installation.

    # noqa: E800
    # {
    #     'id': 1,
    #     'name': 'John Doe',
    #     'description': '',
    #     'gateway_model': 'openmotics',
    #     '_acl': {'configure': {'allowed': True}, 'view': {'allowed': True},
    #             'control': {'allowed': True}},
    #     '_version': 1.0, 'user_role': {'role': 'ADMIN', 'user_id': 1},
    #     'registration_key': 'xxxxx-xxxxx-xxxxxxx',
    #     'platform': 'CLASSIC',
    #     'building_roles': [],
    #     'version': '1.16.5',
    #     'network': {'local_ip_address': '172.16.1.25'},
    #     'flags': {'UNREAD_NOTIFICATIONS': 0, 'ONLINE': None},
    #     'features':
    #         {'outputs': {'available': True, 'used': True, 'metadata': None},
    #          'thermostats': {'available': True, 'used': False, 'metadata': None},
    #          'energy': {'available': True, 'used': True, 'metadata': None},
    #          'apps': {'available': True, 'used': False, 'metadata': None},
    #          'shutters': {'available': True, 'used': False, 'metadata': None},
    #          'consumption': {'available': False, 'used': False, 'metadata': None},
    #          'scheduler': {'available': True, 'used': True, 'metadata': None},
    #          'ems': {'available': False, 'used': False, 'metadata': None}},
    #          'gateway_features': ['metrics', 'dirty_flag', 'scheduling',
    #          'factory_reset', 'isolated_plugins',
    #          'websocket_maintenance', 'shutter_positions',
    #          'ventilation', 'default_timer_disabled',
    #          '100_steps_dimmer', 'input_states']
    # }
    """

    # pylint: disable=too-many-instance-attributes
    name: str
    idx: int = field(metadata=field_options(alias="id"))
    description: str | None = field(default=None)
    gateway_model: str | None = field(default=None)
    acl: Acl | None = field(
        default=None,
        metadata=field_options(alias="_acl"),
    )
    version: str | None = field(
        default=None,
        metadata=field_options(alias="_version"),
    )

    user_role: dict[str, Any] | None = field(default=None)
    registration_key: str | None = field(default=None)
    platform: str | None = field(default=None)
    # TODO @woutercoppens: fix later
    # building_roles: dict[str, Any]  | None = field(default=None)
    network: Network | None = field(default=None)
    flags: dict[str, Any] | None = field(default=None)
    features: dict[str, Any] | None = field(default=None)

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
