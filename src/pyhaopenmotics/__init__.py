"""Module HTTP communication with the OpenMotics API."""

from pyhaopenmotics.cloud.models import Installation

from .errors import (
    AuthenticationError,
    OpenMoticsConnectionError,
    OpenMoticsConnectionSslError,
    OpenMoticsConnectionTimeoutError,
    OpenMoticsError,
)
from .helpers import get_ssl_context
from .localgateway import LocalGateway
from .openmoticscloud import OpenMoticsCloud

__all__ = [
    "AuthenticationError",
    "Installation",
    "LocalGateway",
    "OpenMoticsCloud",
    "OpenMoticsConnectionError",
    "OpenMoticsConnectionSslError",
    "OpenMoticsConnectionTimeoutError",
    "OpenMoticsError",
    "get_ssl_context",
]
