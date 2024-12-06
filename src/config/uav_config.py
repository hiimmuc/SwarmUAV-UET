import os
from datetime import datetime
from pathlib import Path

# Do not change
SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent

# NOTE: Changeable settings
MODE = "simulation"  # "simulation" or "real"

# 1. Allow to connect, stream, detect, record
connection_allows = [True, True, True, True, True, True]
streaming_enables = [True, False, False, False, False, False]
detection_enables = [True, False, False, False, False, False]
recording_enables = [True, True, True, True, True, True]

# 2. UAV settings
AVAIL_UAV_INDEXES = [i for i in range(1, 7)]
RESCUE_UAV_INDEX = 6  # index of the free UAV for rescue mission
INIT_LON = 8.545594545594
INIT_LAT = 47.397823397823
INIT_ALT = [5, 6, 7, 8, 9, 10]  # chang initial altitudes for each UAV

OVERWRITE_PARAMS = {  # Overwrite parameters for each UAV
    1: {
        "MIS_TAKEOFF_ALT": 5,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 2,  # Maximum ground speed
        "CURRENT_SPEED": 1,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
    2: {
        "MIS_TAKEOFF_ALT": 6,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 2,  # Maximum ground speed
        "CURRENT_SPEED": 1,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
    3: {
        "MIS_TAKEOFF_ALT": 7,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 2,  # Maximum ground speed
        "CURRENT_SPEED": 1,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
    4: {
        "MIS_TAKEOFF_ALT": 8,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 2,  # Maximum ground speed
        "CURRENT_SPEED": 1,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
    5: {
        "MIS_TAKEOFF_ALT": 9,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 2,  # Maximum ground speed
        "CURRENT_SPEED": 1,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
    6: {
        "MIS_TAKEOFF_ALT": 10,  # Take-off altitude
        "MPC_TKO_SPEED": 2,  # Takeoff climb rate
        "GND_SPEED_MAX": 5,  # Maximum ground speed
        "CURRENT_SPEED": 2,  # Current speed during a mission, reposition, and similar.
        "RTL_AFTER_MS": True,  # RTL after mission
    },
}

#
MAX_UAV_COUNT = len(AVAIL_UAV_INDEXES)
try:
    AVAIL_UAV_INDEXES.remove(RESCUE_UAV_INDEX)
except Exception as e:
    print(e)

"""Set connection as follows:
- Serial: serial:///path/to/serial/dev[:baudrate]
    Example: serial:///dev/ttyUSB0:57600
    - PROTOCOL: serial
    - SERVER_HOST: /dev/ttyUSB0
    - DEFAULT_SERVER_PORT: 57600
- UDP: udp://[bind_host][:bind_port]
    Example: udp://:14541
    - PROTOCOL: udp
    - SERVER_HOST: 
    - DEFAULT_SERVER_PORT: 14541
- TCP: tcp://[server_host][:server_port]
    Example: tcp://localhost:5760
    - PROTOCOL: tcp
    - SERVER_HOST: localhost
    - DEFAULT_SERVER_PORT: 5760
"""

# UAV connection settings
if MODE == "simulation":
    DEFAULT_PROTOCOL = "udp"
    DEFAULT_SERVER_HOST = ""
    DEFAULT_SERVER_PORT = 14541
    DEFAULT_CLIENT_PORT = 50060
    #
    PROTOCOLS = [DEFAULT_PROTOCOL] * MAX_UAV_COUNT
    SERVER_HOSTS = [DEFAULT_SERVER_HOST] * MAX_UAV_COUNT
    SERVER_PORTS = [DEFAULT_SERVER_PORT + i for i in range(MAX_UAV_COUNT)]
    CLIENT_PORTS = [DEFAULT_CLIENT_PORT + i for i in range(MAX_UAV_COUNT)]
else:  # acm ports for real UAVs
    DEFAULT_PROTOCOL = "serial"
    DEFAULT_SERVER_HOST = "/dev/tty"
    DEFAULT_SERVER_PORT = 57600
    DEFAULT_CLIENT_PORT = 50060
    # NOTE change the following values to match the actual connection
    PROTOCOLS = [DEFAULT_PROTOCOL] * MAX_UAV_COUNT
    SERVER_HOSTS = [
        "/dev/ttyACM0",
        "/dev/ttyACM1",
        "/dev/ttyACM2",
        "/dev/ttyACM3",
        "/dev/ttyACM4",
        "/dev/ttyACM5",
    ]
    SERVER_PORTS = [57600 for _ in range(MAX_UAV_COUNT)]  # same baudrate for all UAVs
    CLIENT_PORTS = [DEFAULT_CLIENT_PORT + i for i in range(MAX_UAV_COUNT)]

SYSTEMS_ADDRESSES = [
    f"{proto}://{server_host}:{server_port}"
    for (proto, server_host, server_port) in zip(PROTOCOLS, SERVER_HOSTS, SERVER_PORTS)
]

# 3. Log settings
plans_log_dir = f"{SRC_DIR}/logs/points/"
parameter_data_files = [
    f"{SRC_DIR}/data/parameters/param_uav_{i}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
