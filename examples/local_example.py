#!/usr/bin/env python3
# noqa: E800
"""Local Example.

How to use this script:
    pip install python-dotenv
    export LOCALGW='192.168.0.2'
    export USER_NAME="dnfqsdfjqsjfqsdjfqf"
    export PASSWORD="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    export TLS=True
    python cloud_example.py
"""
from __future__ import annotations

import asyncio
import os
import ssl

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    raise ImportError("You have to run 'pip install python-dotenv' first") from exc

from pyhaopenmotics import LocalGateway

# noqa: E800
# import certifi
# import logging


ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
# noqa: E800
ssl_context.options &= ~ssl.OP_NO_SSLv3
ssl_context.minimum_version = ssl.TLSVersion.TLSv1
ssl_context.set_ciphers("AES256-SHA")  # enables weaker ciphers and protocols
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# # ssl_context.set_ciphers("DEFAULT:@SECLEVEL=1") # enables weaker ciphers and protocols
# # ssl_context.load_verify_locations(certifi.where())

load_dotenv()

localgw = os.environ["LOCALGW"]
username = os.environ["USER_NAME"]
password = os.environ["PASSWORD"]
port = int(os.environ["PORT"])
tls = bool(os.environ["TLS"])


async def main() -> None:
    """Show example on controlling your OpenMotics device."""
    async with LocalGateway(
        localgw=localgw,
        username=username,
        password=password,
        port=port,
        tls=tls,
        ssl_context=ssl_context,
    ) as omclient:
        # await omclient.login()

        await omclient.exec_action("get_version")

        outputs = await omclient.outputs.get_all()

        if outputs[0].status.on is True:
            pass
        else:
            pass

        await omclient.outputs.get_by_id(0)

        # await omclient.outputs.toggle(0)

        await omclient.sensors.get_all()

        await omclient.shutters.get_all()

        await omclient.groupactions.get_all()

        await omclient.thermostats.groups.get_all()

        await omclient.thermostats.units.get_all()

        await omclient.close()


if __name__ == "__main__":
    asyncio.run(main())
