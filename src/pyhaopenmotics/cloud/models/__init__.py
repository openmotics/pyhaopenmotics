"""Init file for the models."""

from pyhaopenmotics.cloud.models.groupaction import GroupAction
from pyhaopenmotics.cloud.models.input import OMInput
from pyhaopenmotics.cloud.models.installation import Installation
from pyhaopenmotics.cloud.models.light import Light
from pyhaopenmotics.cloud.models.location import Location
from pyhaopenmotics.cloud.models.output import Output
from pyhaopenmotics.cloud.models.sensor import Sensor
from pyhaopenmotics.cloud.models.shutter import Shutter
from pyhaopenmotics.cloud.models.thermostat import ThermostatGroup, ThermostatUnit

__all__ = [
    "GroupAction",
    "Installation",
    "Light",
    "Location",
    "OMInput",
    "Output",
    "Sensor",
    "Shutter",
    "ThermostatGroup",
    "ThermostatUnit",
]
