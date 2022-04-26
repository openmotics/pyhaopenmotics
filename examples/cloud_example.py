#!/usr/bin/env python3
# noqa: E800
"""Cloud example.

How to use this script:
    export CLIENT_ID="dnfqsdfjqsjfqsdjfqf"
    export CLIENT_SECRET="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    python cloud_example.py
"""
from __future__ import annotations

import asyncio
import logging
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    raise ImportError("You have to run 'pip install python-dotenv' first") from exc

try:
    from authlib.integrations.httpx_client import AsyncOAuth2Client
except ModuleNotFoundError as exc:
    raise ImportError("You have to run 'pip install httpx authlib' first") from exc


from pyhaopenmotics import OpenMoticsCloud
from pyhaopenmotics.const import CLOUD_SCOPE, OAUTH2_TOKEN

# UNCOMMENT THIS TO SEE ALL THE HTTPX INTERNAL LOGGING
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(log_format)
log.addHandler(console)


load_dotenv()

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

# base_url = f"{CLOUD_BASE_URL}/{CLOUD_API_VERSION}"

# token_url = f"{base_url}{CLOUD_API_TOKEN_URL}"
# authorize_url = f"{base_url}{CLOUD_API_AUTHORIZATION_URL}"


async def main() -> None:
    """Docstring."""

    token = None

    print(OAUTH2_TOKEN)

    async with AsyncOAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        token_endpoint_auth_method="client_secret_post",  # noqa # nosec
        scope=CLOUD_SCOPE,
        token_endpoint=OAUTH2_TOKEN,
        grant_type="client_credentials",
    ) as httpx_session:

        token = await httpx_session.fetch_token(
            url=OAUTH2_TOKEN,
            grant_type="client_credentials",
        )
        access_token = token.get("access_token")
        print(access_token)

        omclient = OpenMoticsCloud(token=access_token)

        installations = await omclient.installations.get_all()
        print(installations)

        i_id = installations[0].idx

        installation = await omclient.installations.get_by_id(i_id)
        print(installation)
        omclient.installation_id = i_id
        print(installation.idx)
        print(installation.name)

        outputs = await omclient.outputs.get_all()
        print(outputs)

        print(outputs[0])

        sensors = await omclient.sensors.get_all()
        print(sensors)

        gaga = await omclient.groupactions.get_all()
        print(gaga)

        tgga = await omclient.thermostats.groups.get_all()
        print(tgga)

        tuga = await omclient.thermostats.units.get_all()
        print(tuga)

        shutters = await omclient.shutters.get_all()
        print(shutters)

        await omclient.close()


if __name__ == "__main__":
    asyncio.run(main())
