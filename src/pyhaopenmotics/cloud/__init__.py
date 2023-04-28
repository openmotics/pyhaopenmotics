"""Directory holding cloud."""
from pyhaopenmotics.cloud.groupactions import OpenMoticsGroupActions
from pyhaopenmotics.cloud.inputs import OpenMoticsInputs
from pyhaopenmotics.cloud.installations import OpenMoticsInstallations
from pyhaopenmotics.cloud.lights import OpenMoticsLights
from pyhaopenmotics.cloud.outputs import OpenMoticsOutputs
from pyhaopenmotics.cloud.sensors import OpenMoticsSensors
from pyhaopenmotics.cloud.shutters import OpenMoticsShutters
from pyhaopenmotics.cloud.thermostats import OpenMoticsThermostats

__all__ = [
    "OpenMoticsInstallations",
    "OpenMoticsOutputs",
    "OpenMoticsInputs",
    "OpenMoticsGroupActions",
    "OpenMoticsShutters",
    "OpenMoticsLights",
    "OpenMoticsSensors",
    "OpenMoticsThermostats",
]
