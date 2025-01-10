"""Module HTTP communication with the OpenMotics API."""

from pyhaopenmotics.client.errors import (
    AuthenticationError,
    OpenMoticsConnectionError,
    OpenMoticsConnectionSslError,
    OpenMoticsConnectionTimeoutError,
    OpenMoticsError,
)
from pyhaopenmotics.client.localgateway import LocalGateway
from pyhaopenmotics.client.openmoticscloud import OpenMoticsCloud
from pyhaopenmotics.client.websocket import WebsocketClient
from pyhaopenmotics.cloud.models import Installation

__all__ = [
    "AuthenticationError",
    "Installation",
    "LocalGateway",
    "OpenMoticsCloud",
    "OpenMoticsConnectionError",
    "OpenMoticsConnectionSslError",
    "OpenMoticsConnectionTimeoutError",
    "OpenMoticsError",
    "WebsocketClient",
    # "get_ssl_context",
]
