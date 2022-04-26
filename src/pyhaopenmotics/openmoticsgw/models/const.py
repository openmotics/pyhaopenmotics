"""Get a list of all modules attached and registered with the master.

:returns:
    'output': list of module types (O,R,D) and
    'input': list of input module types (I,T,L).
"""
OPENMOTICS_OUTPUT_TYPES = ["O", "R", "D"]
OPENMOTICS_INPUT_TYPES = ["I", "T", "L"]


# https://wiki.openmotics.com/index.php/Modules
OPENMOTICS_OUTPUT_TYPE_TO_NAME = {
    0: "OUTLET",
    1: "VALVE",
    2: "ALARM",
    3: "APPLIANCE",
    4: "PUMP",
    5: "HVAC",
    6: "GENERIC",
    7: "MOTOR",
    8: "VENTILATION",
    255: "LIGHT",
}

OPENMOTICS_MODULE_TYPE_TO_NAME = {
    "O": "OUTPUT",
    "R": "ROLLER",  # Also known as Shutter
    "D": "DIMMER",
    "I": "INPUT",
    "T": "TEMPERATURE",
    "L": "UNKNOWN",
}
