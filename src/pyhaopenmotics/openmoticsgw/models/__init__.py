"""Init file for the models."""

from pyhaopenmotics.openmoticsgw.models.groupaction import GroupAction
from pyhaopenmotics.openmoticsgw.models.input import OMInput
from pyhaopenmotics.openmoticsgw.models.light import Light
from pyhaopenmotics.openmoticsgw.models.location import Location
from pyhaopenmotics.openmoticsgw.models.output import Output
from pyhaopenmotics.openmoticsgw.models.sensor import Sensor
from pyhaopenmotics.openmoticsgw.models.shutter import Shutter
from pyhaopenmotics.openmoticsgw.models.thermostat import (
    ThermostatGroup,
    ThermostatUnit,
)

__all__ = [
    "GroupAction",
    "Light",
    "Location",
    "OMInput",
    "Output",
    "Sensor",
    "Shutter",
    "ThermostatGroup",
    "ThermostatUnit",
]
