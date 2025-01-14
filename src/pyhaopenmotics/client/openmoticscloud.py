"""Module containing a OpenMoticsCloud Client for the OpenMotics API."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aiohttp

# import websocket
# from websockets import connect
from yarl import URL

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from typing_extensions import Self

    from pyhaopenmotics.cloud.models.installation import Installation

from pyhaopenmotics.client.baseclient import BaseClient
from pyhaopenmotics.cloud.groupactions import OpenMoticsGroupActions
from pyhaopenmotics.cloud.inputs import OpenMoticsInputs
from pyhaopenmotics.cloud.installations import OpenMoticsInstallations
from pyhaopenmotics.cloud.lights import OpenMoticsLights
from pyhaopenmotics.cloud.outputs import OpenMoticsOutputs
from pyhaopenmotics.cloud.sensors import OpenMoticsSensors
from pyhaopenmotics.cloud.shutters import OpenMoticsShutters
from pyhaopenmotics.cloud.thermostats import OpenMoticsThermostats
from pyhaopenmotics.const import CLOUD_API_URL

# from .helpers import base64_encode

_LOGGER = logging.getLogger(__name__)


class OpenMoticsCloud(BaseClient):
    """Docstring."""

    _installations: list[Installation] | None

    def __init__(
        self,
        token: str,
        *,
        request_timeout: int = 8,
        session: aiohttp.client.ClientSession | None = None,
        token_refresh_method: Callable[[], Awaitable[str]] | None = None,
        installation_id: int | None = None,
        base_url: str = CLOUD_API_URL,
    ) -> None:
        """Initialize connection with the OpenMotics Cloud API.

        Args:
        ----
            token: str
            request_timeout: int
            session: aiohttp.client.ClientSession
            token_refresh_method: token refresh function
            installation_id: int
            base_url: str

        """
        super().__init__(
            token=token,
            request_timeout=request_timeout,
            session=session,
        )
        self._installation_id = installation_id
        self.base_url = base_url

    @property
    def installation_id(self) -> int | None:
        """Get installation id.

        Returns
        -------
            The installation id that will be used for this session.

        """
        return self._installation_id

    @installation_id.setter
    def installation_id(self, installation_id: int) -> None:
        """Set installation id.

        Args:
        ----
            installation_id: The installation id that will be used
                for this session.

        """
        self._installation_id = installation_id

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
        url = URL(f"{self.base_url}{path}")
        if scheme != "https":
            url = URL(url).with_scheme(scheme)
        return str(url)

    # async def subscribe_webhook(self) -> None:
    #     """Register a webhook with OpenMotics for live updates."""
    #     # Register webhook
    #     await self._request(
    #         "/ws/events",
    #                 "types": [
    #                     "OUTPUT_CHANGE",
    #                     "SENSOR_CHANGE",
    #                     "SHUTTER_CHANGE",
    #                     "THERMOSTAT_CHANGE",
    #                     "THERMOSTAT_GROUP_CHANGE",
    #                     "VENTILATION_CHANGE",
    #                 ],
    #             },
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
        # if self.token is None or self.token_expires_at < time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC:

        if headers is None:
            headers = {}

        headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept": "application/json",
                # "Accept-Language": "en-US,en;q=0.5",
                # "Accept-Encoding": "gzip, defalte, br",
                # "Referer": "https://portal.openmotics.com/",
                "Authorization": f"Bearer {self.token}",
                # "Content-Type": "application/json",
                # "Origin": "https://portal.openmotics.com",
                # "Connection": "keep-alive",
                # "Sec-Fetch-Dest": "empty",
                # "Sec-Fetch-Mode": "cors",
                # "Sec-Fetch-Site": "same-site",
                # "Cache-Control": "no-cache",
            },
        )
        return headers

    async def _get_ws_connection_url(self) -> str:
        return await self._get_url(
            path="/ws/events",
            scheme="wss",
        )

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
        # if self.token is None or self.token_expires_at < time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC:

        if headers is None:
            headers = {}

        b64token = base64_encode(self.token)

        headers.update(
            {
                # "User-Agent": self.user_agent,
                # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                # "Accept-Language": "en-US,en;q=0.5",
                # "Accept-Encoding": "gzip, defalte, br",
                "Sec-WebSocket-Protocol": f"authorization.bearer.{b64token}",
                "Sec-WebSocket-extensions": "permessage-deflate",
                "Sec-Fetch-Dest": "websocket",
                "Sec-Fetch-Mode": "websocket",
                "Sec-Fetch-site": "same-site",
                # "cache-control": "no-cache",
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

    #     ctx = ssl.SSLContext()  # ssl.PROTOCOL_TLSv1_2)
    #     ctx.check_hostname = False

    #     try:
    #         self._wsclient = await self.session.ws_connect(
    #             url=url,
    #             headers=headers,
    #             ssl=ctx,
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

    #     _LOGGER.debug(f"uri: {uri}")
    #     _LOGGER.debug(f"extra_headers: {extra_headers}")
    #     try:
    #         async with connect(
    #             uri=uri,
    #             extra_headers=extra_headers,
    #         ) as ws:
    #             _LOGGER.debug("WebSocket Opened.")
    #             await ws.send(
    #                 json.dumps(
    #                     {
    #                         "type": "ACTION",
    #                         "data": {
    #                             "action": "set_subscription",
    #                             "types": [
    #                                 "OUTPUT_CHANGE",
    #                                 "SENSOR_CHANGE",
    #                                 "SHUTTER_CHANGE",
    #                                 "THERMOSTAT_CHANGE",
    #                                 "THERMOSTAT_GROUP_CHANGE",
    #                                 "VENTILATION_CHANGE",
    #                                 "INPUT_TRIGGER",
    #                             ],
    #                             "installation_ids": self.installation_id,
    #                         },
    #                     },
    #                 ),
    #             )
    #             _LOGGER.debug(json.loads(await ws.recv()))
    #             _LOGGER.debug("websocket client connected. looping...")

    #             while self.loop:
    #                 data = json.loads(await ws.recv())
    #                 if "event" not in data:
    #                     continue

    #                 try:
    #                     self.ws_handler(self, data)
    #                 except:
    #                     _LOGGER.error("".join(traceback.format_exc()))

    #     except asyncio.exceptions.TimeoutError:
    #         pass

    # async def connect3(self) -> None:
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

    #     _LOGGER.debug(f"uri: {uri}")
    #     _LOGGER.debug(f"extra_headers: {extra_headers}")

    #     def on_message(ws, message):
    #         print(message)

    #     def on_error(ws, error):
    #         print(error)

    #     def on_close(ws, close_status_code, close_msg):
    #         print("### closed ###")

    #     def on_open(ws):
    #         print("Opened connection")

    #     def on_ping(ws, message):
    #         print("Got a ping! A pong reply has already been automatically sent.")

    #     def on_pong(ws, message):
    #         print("Got a pong! No need to respond")

    #     websocket.enableTrace(True)
    #     base64_message = base64_encode(self.token)

    #     print("connecting")
    #     ws = websocket.create_connection(
    #         uri,
    #         origin="https://portal.openmotics.com",
    #         header=extra_headers,
    #         subprotocols=[f"authorization.bearer.{base64_message}"],
    #     )
    #     print("connected")
    #     _LOGGER.debug("WebSocket Opened.")
    #     ws.send(
    #         json.dumps(
    #             {
    #                 "type": "ACTION",
    #                 "data": {
    #                     "action": "set_subscription",
    #                     "types": [
    #                         "OUTPUT_CHANGE",
    #                         "SENSOR_CHANGE",
    #                         "SHUTTER_CHANGE",
    #                         "THERMOSTAT_CHANGE",
    #                         "THERMOSTAT_GROUP_CHANGE",
    #                         "VENTILATION_CHANGE",
    #                         "INPUT_TRIGGER",
    #                     ],
    #                     "installation_ids": self.installation_id,
    #                 },
    #             },
    #         ),
    #     )
    #     _LOGGER.debug(json.loads(await ws.recv()))

    #     # ws = websocket.WebSocketApp(uri,

    @property
    def installations(self) -> OpenMoticsInstallations:
        """Get installations.

        Returns
        -------
            OpenMoticsInstallations

        """
        return OpenMoticsInstallations(self)

    @property
    def inputs(self) -> OpenMoticsInputs:
        """Get inputs.

        Returns
        -------
            OpenMoticsInputs

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

    async def get(
        self, path: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        """Make get request using the underlying aiohttp.ClientSession.

        Args:
        ----
            path: string
            **kwargs: any

        Returns:
        -------
            response json or text

        """
        headers = await self._get_auth_headers(headers)
        return await self._request(
            path,
            method=aiohttp.hdrs.METH_GET,
            headers=headers,
            **kwargs,
        )

    async def post(
        self, path: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        """Make get request using the underlying aiohttp.ClientSession.

        Args:
        ----
            path: path
            **kwargs: extra args

        Returns:
        -------
            response json or text

        """
        headers = await self._get_auth_headers(headers)
        return await self._request(
            path,
            method=aiohttp.hdrs.METH_POST,
            **kwargs,
        )

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            OpenMoticsCloud: The OpenMoticsCloud object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            *_exc_info: Exec type.

        """
        await self.close()
