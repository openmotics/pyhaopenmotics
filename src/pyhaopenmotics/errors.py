"""Exceptions for the OpenMotics API."""


class OpenMoticsError(Exception):

    """Generic OpenMotics exception."""


class OpenMoticsConnectionSslError(OpenMoticsError):

    """OpenMotics connection SSL exception."""


class OpenMoticsConnectionError(OpenMoticsError):

    """OpenMotics connection exception."""


class OpenMoticsConnectionTimeoutError(OpenMoticsConnectionError):

    """OpenMotics connection Timeout exception."""


class AuthenticationException(Exception):

    """Exception is raised when the user credentials are not valid."""
