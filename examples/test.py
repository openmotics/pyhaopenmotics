#!/usr/bin/env python3
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
import logging
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    msg = "You have to run 'pip install python-dotenv' first"
    raise ImportError(msg) from exc

from pyhaopenmotics import LocalGateway

# UNCOMMENT THIS TO SEE ALL THE HTTPX INTERNAL LOGGING
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(log_format)
log.addHandler(console)


load_dotenv()

localgw = os.environ["LOCALGW"]
username = os.environ["USER_NAME"]
password = os.environ["PASSWORD"]
port = int(os.environ["PORT"])


async def main() -> None:
    """Show example on controlling your OpenMotics device."""
    async with LocalGateway(
        localgw=localgw,
        username=username,
        password=password,
        port=port,
    ) as omclient:
        await omclient.exec_action("get_version")

        outputs = await omclient.outputs.get_all()

        # if outputs[0].status.on is True:
        #     pass
        # else:
        #     pass

        # await omclient.outputs.get_by_id(0)

        #         await omclient.inputs.get_all()

        #        await omclient.sensors.get_all()

        #        await omclient.shutters.get_all()

        #        await omclient.groupactions.get_all()

        #        await omclient.thermostats.groups.get_all()

        #        await omclient.thermostats.units.get_all()

        print("New API -----------------------------------------------------------")

        # await omclient.get('/api/thermostat/control')
        await omclient.get("/api/thermostat/config")

        await omclient.get("/api/thermostat/config/2")

        await omclient.get("/api/sensors")

        await omclient.close()


if __name__ == "__main__":
    asyncio.run(main())
