"""
UAV Configuration Module

This module defines configuration settings for UAV connectivity, flight parameters,
and mission settings for both simulation and real-world UAV operations.
"""

import os
from pathlib import Path

# Base paths (do not change)
SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent

# -------------------------------- OPERATION MODE --------------------------------
# "simulation" for virtual UAVs, "real" for physical hardware
MODE = "simulation"  # Options: "simulation" or "real"

# -------------------------------- UAV ENABLING --------------------------------
# Enable/disable features for each UAV (True=enabled, False=disabled)
connection_allows = [True, True, True, True, True, True]  # Allow connection to UAVs
streaming_enables = [True, False, False, False, False, False]  # Enable video streams
detection_enables = [True, False, False, False, False, False]  # Enable object detection
recording_enables = [True, True, True, True, True, True]  # Enable video recording

# -------------------------------- UAV INDEXES AND POSITIONS --------------------------------
# Available UAV indexes (1-based)
AVAIL_UAV_INDEXES = [i for i in range(1, 7)]
RESCUE_UAV_INDEX = 6  # Index of the UAV designated for rescue missions

# Initial positions for all UAVs
INIT_LON = 8.545594545594  # Initial longitude
INIT_LAT = 47.397823397823  # Initial latitude
INIT_ALT = [5, 6, 7, 8, 9, 10]  # Initial altitudes for each UAV (meters)

# -------------------------------- FLIGHT PARAMETERS --------------------------------
# Overwrite parameters for each UAV
OVERWRITE_PARAMS = {
    1: {
        "MIS_TAKEOFF_ALT": 5,    # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 2,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 1,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
    2: {
        "MIS_TAKEOFF_ALT": 6,    # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 2,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 1,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
    3: {
        "MIS_TAKEOFF_ALT": 7,    # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 2,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 1,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
    4: {
        "MIS_TAKEOFF_ALT": 8,    # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 2,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 1,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
    5: {
        "MIS_TAKEOFF_ALT": 9,    # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 2,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 1,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
    6: {
        "MIS_TAKEOFF_ALT": 10,   # Take-off altitude (m)
        "MPC_TKO_SPEED": 2,      # Takeoff climb rate (m/s)
        "GND_SPEED_MAX": 5,      # Maximum ground speed (m/s)
        "CURRENT_SPEED": 2,      # Current speed during mission (m/s)
        "RTL_AFTER_MS": True,    # Return to launch after mission
    },
}

# Calculate max UAV count and remove rescue UAV from available list
MAX_UAV_COUNT = len(AVAIL_UAV_INDEXES)
try:
    AVAIL_UAV_INDEXES.remove(RESCUE_UAV_INDEX)
except Exception as e:
    print(f"Warning: Could not remove rescue UAV from available list: {e}")

# -------------------------------- CONNECTION SETTINGS --------------------------------
"""
Connection Format Reference:
- Serial: serial:///path/to/serial/dev[:baudrate]
    Example: serial:///dev/ttyUSB0:57600
    - PROTOCOL: serial
    - SERVER_HOST: /dev/ttyUSB0
    - SERVER_PORT: 57600
- UDP: udp://[bind_host][:bind_port]
    Example: udp://:14541
    - PROTOCOL: udp
    - SERVER_HOST: (empty)
    - SERVER_PORT: 14541
- TCP: tcp://[server_host][:server_port]
    Example: tcp://localhost:5760
    - PROTOCOL: tcp
    - SERVER_HOST: localhost
    - SERVER_PORT: 5760
"""

# Configure UAV connection settings based on mode
if MODE == "simulation":
    # Simulation mode uses UDP connections
    DEFAULT_PROTOCOL = "udp"
    DEFAULT_SERVER_HOST = ""
    DEFAULT_SERVER_PORT = 14541
    DEFAULT_CLIENT_PORT = 50060
    
    # Generate connection settings for all UAVs
    PROTOCOLS = [DEFAULT_PROTOCOL] * MAX_UAV_COUNT
    SERVER_HOSTS = [DEFAULT_SERVER_HOST] * MAX_UAV_COUNT
    SERVER_PORTS = [DEFAULT_SERVER_PORT + i for i in range(MAX_UAV_COUNT)]
    CLIENT_PORTS = [DEFAULT_CLIENT_PORT + i for i in range(MAX_UAV_COUNT)]
    
else:  # Real mode uses serial connections
    DEFAULT_PROTOCOL = "serial"
    DEFAULT_SERVER_HOST = "/dev/tty"
    DEFAULT_SERVER_PORT = 57600
    DEFAULT_CLIENT_PORT = 50060
    
    # NOTE: Adjust these values to match actual hardware connections
    PROTOCOLS = [DEFAULT_PROTOCOL] * MAX_UAV_COUNT
    SERVER_HOSTS = [
        "/dev/ttyACM0",
        "/dev/ttyACM1",
        "/dev/ttyACM2",
        "/dev/ttyACM3",
        "/dev/ttyACM4",
        "/dev/ttyACM5",
    ]
    SERVER_PORTS = [57600] * MAX_UAV_COUNT  # Same baudrate for all UAVs
    CLIENT_PORTS = [DEFAULT_CLIENT_PORT + i for i in range(MAX_UAV_COUNT)]

# Generate complete system addresses for MAVSDK
SYSTEMS_ADDRESSES = [
    f"{proto}://{server_host}:{server_port}"
    for (proto, server_host, server_port) in zip(PROTOCOLS, SERVER_HOSTS, SERVER_PORTS)
]

# -------------------------------- LOG SETTINGS --------------------------------
# Create directory structure for logs and data
plans_log_dir = f"{SRC_DIR}/logs/points/"
parameter_uav_dir = f"{SRC_DIR}/data/parameters/"
drone_init_pos_dir = f"{SRC_DIR}/logs/drone_init_pos/"
drone_current_pos_dir = f"{SRC_DIR}/logs/drone_current_pos/"

# Create directories if they don't exist
os.makedirs(plans_log_dir, exist_ok=True)
os.makedirs(parameter_uav_dir, exist_ok=True)
os.makedirs(drone_init_pos_dir, exist_ok=True)
os.makedirs(drone_current_pos_dir, exist_ok=True)

# File paths for parameters and initial positions
parameter_data_files = [
    f"{SRC_DIR}/data/parameters/param_uav_{i}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
drone_init_pos_files = [
    f"{SRC_DIR}/logs/drone_init_pos/uav_{i}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
drone_current_pos_files = [
    f"{SRC_DIR}/logs/drone_current_pos/uav_{i}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
