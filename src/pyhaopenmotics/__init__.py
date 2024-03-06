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
    "OpenMoticsCloud",
    "LocalGateway",
    "OpenMoticsError",
    "OpenMoticsConnectionError",
    "OpenMoticsConnectionTimeoutError",
    "OpenMoticsConnectionSslError",
    "AuthenticationError",
    "Installation",
    "WebsocketClient",
    # "get_ssl_context",
]
