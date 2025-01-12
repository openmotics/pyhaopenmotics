"""Installation Model for the OpenMotics API."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Allowed(BaseModel):

    """Object holding an OpenMotics Installation."""

    allowed: bool | None


class Acl(BaseModel):

    """Object holding an OpenMotics Installation."""

    configure: Allowed | None
    view: Allowed | None
    control: Allowed | None


class Network(BaseModel):

    """Object holding an OpenMotics Installation."""

    local_ip_address: str | None


class Installation(BaseModel):

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
    idx: int = Field(..., alias="id")
    name: str
    description: str | None
    gateway_model: str | None
    acl: Acl = Field(..., alias="_acl")
    version: str = Field(..., alias="_version")
    user_role: dict[str, Any] | None
    registration_key: str | None
    platform: str | None
    building_roles: dict[str, Any] | None
    network: Network | None
    flags: dict[str, Any] | None
    features: dict[str, Any] | None

    def __str__(self) -> str:
        """Represent the class objects as a string.

        Returns
        -------
            string

        """
        return f"{self.idx}_{self.name}"
