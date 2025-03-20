"""
Interface Configuration Module

This module defines paths, screen sizes, and parameter lists for the UAV control interface.
"""

import os
from datetime import datetime
from pathlib import Path

# cSpell:ignore baudrate, uav, rtl, opencv, cv2, fourcc, rtsp, uet, YOLO, nosignal, XVID

# Base paths (do not change)
SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent

# Current timestamp for logging, filenames, etc.
NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Maximum number of UAVs supported
MAX_UAV_COUNT = 6

# Screen size configuration for different views
screen_sizes = {
    "general_screen": (640, 360),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}

# Logo and application icon paths
logo1_path = f"{ROOT_DIR}/assets/icons/logo1.png"
logo2_path = f"{ROOT_DIR}/assets/icons/logoUET.png"
app_icon_path = f"{ROOT_DIR}/assets/icons/app.png"

# Button icon paths
connect_icon_path = f"{SRC_DIR}/Qt/icons/connect.png"
arm_icon_path = f"{SRC_DIR}/Qt/icons/arm.png"
disarm_icon_path = f"{SRC_DIR}/Qt/icons/disarm.png"
takeoff_icon_path = f"{SRC_DIR}/Qt/icons/takeOff.png"
landing_icon_path = f"{SRC_DIR}/Qt/icons/landing.png"
mission_icon_path = f"{SRC_DIR}/Qt/icons/mission.png"
pause_icon_path = f"{SRC_DIR}/Qt/icons/pauseMission.png"
push_mission_icon_path = f"{SRC_DIR}/Qt/icons/pushMission.png"
return_icon_path = f"{SRC_DIR}/Qt/icons/return.png"
rtl_icon_path = f"{SRC_DIR}/Qt/icons/rtl.png"
toggle_icon_path = f"{SRC_DIR}/Qt/icons/toggle_camera.png"
open_close_icon_path = f"{SRC_DIR}/Qt/icons/toggle_open.png"

# Default screen images for different view types
noSignal_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/nosignal_{w}x{h}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/pause_screen_{w}x{h}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths["all"] = f"{ROOT_DIR}/assets/pictures/pause_screen.jpg"

# Map HTML file paths
map_html_path = f"file://{ROOT_DIR}/assets/map.html"
map_html_updated_path = f"file://{SRC_DIR}/data/map.html"

map_ovv_html_path = f"file://{ROOT_DIR}/assets/map_ovv.html"
map_ovv_html_updated_path = f"file://{SRC_DIR}/data/map.html"

# PX4 parameters to display in the interface
displayed_parameter_list = [
    "MIS_TAKEOFF_ALT",  # Take-off altitude
    "COM_DISARM_LAND",  # Time-out for auto disarm after landing
    "MPC_TKO_SPEED",    # Takeoff climb rate
    "MPC_LAND_SPEED",   # Landing descend rate
    "MPC_XY_P",         # Proportional gain for horizontal position error
    "MPC_XY_VEL_P_ACC", # Proportional gain for horizontal velocity error
    "MPC_XY_VEL_D_ACC", # Derivative gain for horizontal velocity error
    "MC_PITCH_P",       # Pitch P gain
    "MC_ROLL_P",        # Roll P gain
    "MC_YAW_P",         # Yaw P gain
]