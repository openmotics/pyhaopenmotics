"""Module containing a LocalGateway Client for the OpenMotics API."""

from __future__ import annotations

import logging
import ssl
import time
from typing import Any

import aiohttp
from yarl import URL

from pyhaopenmotics.client.baseclient import BaseClient
from pyhaopenmotics.helpers import get_ssl_context
from pyhaopenmotics.openmoticsgw.energy import OpenMoticsEnergySensors
from pyhaopenmotics.openmoticsgw.groupactions import OpenMoticsGroupActions
from pyhaopenmotics.openmoticsgw.inputs import OpenMoticsInputs
from pyhaopenmotics.openmoticsgw.lights import OpenMoticsLights
from pyhaopenmotics.openmoticsgw.outputs import OpenMoticsOutputs
from pyhaopenmotics.openmoticsgw.sensors import OpenMoticsSensors
from pyhaopenmotics.openmoticsgw.shutters import OpenMoticsShutters
from pyhaopenmotics.openmoticsgw.thermostats import OpenMoticsThermostats

_LOGGER = logging.getLogger(__name__)

LOCAL_TOKEN_EXPIRES_IN = 3600
CLOCK_OUT_OF_SYNC_MAX_SEC = 20


class LocalGateway(BaseClient):
    """Docstring."""

    def __init__(
        self,
        username: str,
        password: str,
        localgw: str,
        *,
        request_timeout: int = 8,
        session: aiohttp.client.ClientSession | None = None,
        verify_ssl: bool = False,
        ssl_context: ssl.SSLContext | None = None,
        port: int = 443,
    ) -> None:
        """Initialize connection with the OpenMotics LocalGateway API.

        Args:
        ----
            localgw: Hostname or IP address of the AdGuard Home instance.
            password: Password for HTTP auth, if enabled.
            port: Port on which the API runs, usually 3000.
            request_timeout: Max timeout to wait for a response from the API.
            session: Optional, shared, aiohttp client session.
            tls: True, when TLS/SSL should be used.
            username: Username for HTTP auth, if enabled.
            ssl_context: ssl.SSLContext.

        """
        super().__init__(
            request_timeout=request_timeout,
            session=session,
            port=port,
            verify_ssl=verify_ssl,
        )

        self.localgw = localgw
        self.password = password
        self.username = username

        if ssl_context is not None:
            self.ssl_context = ssl_context
        else:
            self.ssl_context = get_ssl_context(verify_ssl=verify_ssl)

        self.auth = None
        if self.username and self.password:
            _LOGGER.debug("LocalGateway setting self.auth")
            self.auth = {"username": self.username, "password": self.password}

    async def exec_action(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        """Make get request using the underlying aiohttp.ClientSession.

        Args:
        ----
            path: path
            data: dict
            headers: dict

        Returns:
        -------
            response json or text

        """
        # Try to execute the action.
        return await self._request(
            path,
            method=aiohttp.hdrs.METH_POST,
            data=data,
            headers=await self._get_auth_headers(headers),
        )

    async def get_token(self) -> None:
        """Login to the gateway: sets the token in the connector."""
        resp = await self._request(
            path="login",
            data=self.auth,
        )
        if resp["success"] is True:
            self.token = resp["token"]
            self.token_expires_at = time.time() + LOCAL_TOKEN_EXPIRES_IN
        else:
            self.token = None
            self.token_expires_at = 0

    async def _get_url(self, path: str, scheme: str = "https") -> str:
        """Update the auth headers to include a working token.

        Args:
        ----
            path: str
            scheme: str

        Returns:
        -------
            url: str

        """
        url = str(
            URL.build(scheme=scheme, host=self.localgw, port=self.port, path="/").join(
                URL(path)
            ),
        )
        return url

    # async def subscribe_webhook(self, installation_id: str) -> None:
    #     """Register a webhook with OpenMotics for live updates.

    #     Args:
    #     ----

    #     """
    #     # Register webhook
    #     await self._request(
    #         "/ws/events",
    #             "types": [
    #                 "OUTPUT_CHANGE",
    #                 "SHUTTER_CHANGE",
    #                 "THERMOSTAT_CHANGE",
    #                 "THERMOSTAT_GROUP_CHANGE",
    #             ],
    #         },

    # async def unsubscribe_webhook(self) -> None:
    #     """Delete all webhooks for this application ID."""
    #     await self._request(
    #         "/ws/events",

    async def _get_auth_headers(
        self,
        headers: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update the auth headers to include a working token.

        Args:
        ----
            headers: dict

        Returns:
        -------
            headers

        """
        if (
            self.token is None
            or self.token_expires_at < time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC
        ):
            await self.get_token()

        if headers is None:
            headers = {}

        headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept": "application/json, text/plain, */*",
                "Authorization": f"Bearer {self.token}",
            },
        )
        return headers

    async def _get_ws_connection_url(self) -> str:
        url = await self._get_url(
            path="/ws_events",
            scheme="wss",
        )
        return url

    async def _get_ws_headers(
        self,
        headers: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update the auth headers to include a working token.

        Args:
        ----
            headers: dict

        Returns:
        -------
            headers

        """
        if (
            self.token is None
            or self.token_expires_at < time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC
        ):
            await self.get_token()

        if headers is None:
            headers = {}

        base64_message = base64_encode(self.token)

        headers.update(
            {
                # "User-Agent": self.user_agent,
                "Sec-WebSocket-Protocol": f"authorization.bearer.{base64_message}",
                # "Sec-WebSocket-Extensions": "permessage-deflate",
                # "host": self.localgw,
                # "Origin": self.localgw,
                "Connection": "Upgrade",
                "Upgrade": "websocket",
                # "accept-encoding": "gzip, deflate, br",
                # "cache-control": "no-cache",
                # "pragma": "no-cache",
                # # "Sec-Fetch-Dest": "websocket",
                # "Sec-Fetch-Mode": "websocket",
                # "Sec-Fetch-site": "same-site",
                # "user-agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            },
        )
        return headers

    # @property
    # def connected(self) -> bool:
    #     """Return if we are connect to the WebSocket of OpenMotics.

    #     Returns
    #     -------
    #         True if we are connected to the WebSocket,
    #         False otherwise.
    #     """
    #     return self._wsclient is not None and not self._wsclient.closed

    # async def connect(self) -> None:
    #     """Connect to the WebSocket of OpenMotics.

    #     Raises
    #     ------
    #         OpenMoticsError: The configured localgw does not support WebSocket
    #             communications.
    #         OpenMoticsConnectionError: Error occurred while communicating with
    #             OpenMotics via the WebSocket.
    #     """
    #     if self.connected:
    #         return

    #     # if not self._device:

    #     if not self.session:
    #         raise OpenMoticsConnectionError(
    #             "The OM device at {self.localgw} does not support WebSockets",
    #         )

    #     url = await self._get_url(
    #         path="/ws/events",
    #         scheme="wss",
    #     )
    #     headers = await self._get_ws_headers()

    #     try:
    #         self._wsclient = await self.session.ws_connect(
    #             url=url,
    #             headers=headers,
    #             ssl=self.ssl_context,
    #         )
    #     except (
    #         aiohttp.WSServerHandshakeError,
    #         aiohttp.ClientConnectionError,
    #         socket.gaierror,
    #     ) as exception:
    #         raise OpenMoticsConnectionError(
    #             ("Error occurred while communicating with OpenMotics" f" on WebSocket at {url}",),
    #         ) from exception

    # async def connect2(self) -> None:
    #     """Connect to the WebSocket of OpenMotics.

    #     Raises
    #     ------
    #         OpenMoticsError: The configured localgw does not support WebSocket
    #             communications.
    #         OpenMoticsConnectionError: Error occurred while communicating with
    #             OpenMotics via the WebSocket.
    #     """
    #     if self.connected:
    #         return

    #     # if not self._device:

    #     if not self.session:
    #         raise OpenMoticsConnectionError(
    #             "The OM device at {self.localgw} does not support WebSockets",
    #         )

    #     uri = await self._get_url(
    #         path="/ws/events",
    #         scheme="wss",
    #     )
    #     extra_headers = await self._get_ws_headers()

    #     try:
    #         async with websockets.connect(
    #             uri=uri,
    #             extra_headers=extra_headers,
    #             ssl=self.ssl_context,
    #         ) as websocket:
    #             _LOGGER.info("WebSocket Opened.")
    #             _LOGGER.info(json.loads(await websocket.recv()))
    #             _LOGGER.info("websocket client connected. looping...")

    #             while self.loop:
    #                 data = json.loads(await websocket.recv())
    #                 if "event" not in data:
    #                     continue

    #                 try:
    #                     self.ws_handler(self, data)
    #                 except:
    #                     _LOGGER.error("".join(traceback.format_exc()))

    #     except websockets.WebSocketException:
    #         pass

    @property
    def inputs(self) -> OpenMoticsInputs:
        """Get outputs.

        Returns
        -------
            OpenMoticsOutputs

        """
        return OpenMoticsInputs(self)

    @property
    def outputs(self) -> OpenMoticsOutputs:
        """Get outputs.

        Returns
        -------
            OpenMoticsOutputs

        """
        return OpenMoticsOutputs(self)

    @property
    def groupactions(self) -> OpenMoticsGroupActions:
        """Get groupactions.

        Returns
        -------
            OpenMoticsGroupActions

        """
        return OpenMoticsGroupActions(self)

    @property
    def lights(self) -> OpenMoticsLights:
        """Get lights.

        Returns
        -------
            OpenMoticsLights

        """
        # implemented to be compatible with cloud
        return OpenMoticsLights(self)

    @property
    def sensors(self) -> OpenMoticsSensors:
        """Get sensors.

        Returns
        -------
            OpenMoticsSensors

        """
        return OpenMoticsSensors(self)

    @property
    def energysensors(self) -> OpenMoticsEnergySensors:
        """Get energy sensors.

        Returns
        -------
            OpenMoticsEnergySensors

        """
        return OpenMoticsEnergySensors(self)

    @property
    def shutters(self) -> OpenMoticsShutters:
        """Get shutters.

        Returns
        -------
            OpenMoticsShutters

        """
        return OpenMoticsShutters(self)

    @property
    def thermostats(self) -> OpenMoticsThermostats:
        """Get thermostats.

        Returns
        -------
            OpenMoticsThermostats

        """
        return OpenMoticsThermostats(self)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> LocalGateway:
        """Async enter.

        Returns
        -------
            LocalGateway: The LocalGateway object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            *_exc_info: Exec type.

        """
        await self.close()
