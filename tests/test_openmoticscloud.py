"""Asynchronous client for the OpenMotics API."""
# flake8: noqa
# pylint: disable=protected-access
# # mypy: ignore-errors
import asyncio
import socket

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyhaopenmotics import OpenMoticsCloud
from pyhaopenmotics.const import CLOUD_API_VERSION, CLOUD_BASE_URL
from pyhaopenmotics.errors import OpenMoticsConnectionError, OpenMoticsError

get_token_data_request = {
    "grant_type": "client_credentials",
    "client_id": "abc",
    "client_secret": "abc",
}

get_installations_data_request = {
    "access_token": "12345",
}


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout."""
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faking a timeout by sleeping
    async def response_handler(_):  # type: ignore
        """Test request timeout."""
        await asyncio.sleep(2)
        return aresponses.Response(body="Goodmorning!")

    aresponses.add(CLOUD_BASE_URL, CLOUD_API_VERSION, "POST", response_handler)

    async with aiohttp.ClientSession() as session:
        open_motics = OpenMoticsCloud(
            session=session,
            token="12345",
            request_timeout=1,
        )
        with pytest.raises(OpenMoticsConnectionError):
            assert await open_motics._request("/")


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_http_error400(aresponses: ResponsesMockServer) -> None:
    """Test HTTP 404 response handling."""
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aresponses.add(
        CLOUD_BASE_URL,
        CLOUD_API_VERSION,
        "GET",
        aresponses.Response(text="OMG PUPPIES!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        open_motics = OpenMoticsCloud(session=session, token="12345")
        with pytest.raises(OpenMoticsError):
            assert await open_motics._request("/")


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_http_error500(aresponses: ResponsesMockServer) -> None:
    """Test HTTP 500 response handling."""
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aresponses.add(
        CLOUD_BASE_URL,
        CLOUD_API_VERSION,
        "GET",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        open_motics = OpenMoticsCloud(session=session, token="12345")
        with pytest.raises(OpenMoticsError):
            assert await open_motics._request("/")
