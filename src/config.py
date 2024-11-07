import os
from datetime import datetime
from pathlib import Path

# cSpell:ignore baudrate, uav, rtl, opencv, cv2, fourcc, rtsp, uet, YOLO, nosignal, XVID


# Do not change
SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# NOTE: No change: Config for displaying screen
screen_sizes = {
    "general_screen": (640, 360),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}

logo1_path = f"{ROOT_DIR}/assets/icons/logo1.png"
logo2_path = f"{ROOT_DIR}/assets/icons/logoUET.png"
app_icon_path = f"{ROOT_DIR}/assets/icons/app.png"

connect_icon_path = f"{SRC_DIR}/UI/icons/connect.png"
arm_icon_path = f"{SRC_DIR}/UI/icons/arm.png"
disarm_icon_path = f"{SRC_DIR}/UI/icons/disarm.png"
takeoff_icon_path = f"{SRC_DIR}/UI/icons/takeOff.png"
landing_icon_path = f"{SRC_DIR}/UI/icons/landing.png"
mission_icon_path = f"{SRC_DIR}/UI/icons/mission.png"
pause_icon_path = f"{SRC_DIR}/UI/icons/pauseMission.png"
push_mission_icon_path = f"{SRC_DIR}/UI/icons/pushMission.png"
return_icon_path = f"{SRC_DIR}/UI/icons/return.png"
rtl_icon_path = f"{SRC_DIR}/UI/icons/rtl.png"
toggle_icon_path = f"{SRC_DIR}/UI/icons/toggle_camera.png"
open_close_icon_path = f"{SRC_DIR}/UI/icons/toggle_open.png"

noSignal_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/nosignal_{w}x{h}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/pause_screen_{w}x{h}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths["all"] = f"{ROOT_DIR}/assets/pictures/pause_screen.jpg"

map_html_path = f"file://{ROOT_DIR}/assets/map.html"
map_html_updated_path = f"file://{SRC_DIR}/data/map.html"

plans_log_dir = f"{SRC_DIR}/logs/points/"

# parameters
parameter_list = [
    "MIS_TAKEOFF_ALT",
    "COM_DISARM_LAND",
    "MPC_TKO_SPEED",
    "MPC_LAND_SPEED",
    "MPC_XY_P",
    "MPC_XY_VEL_P_ACC",
    "MPC_XY_VEL_D_ACC",
    "MC_PITCH_P",
    "MC_ROLL_P",
    "MC_YAW_P",
]


# Changeable settings
MODE = "simulation"  # "simulation" or "real"

# UAV settings
MAX_UAV_COUNT = 6
FREE_UAV_INDEX = (
    6  # index of the free UAV connect -> arm -> takeoff -> mission -> return -> disarm
)

INIT_LON = 8.545594
INIT_LAT = 47.397823
INIT_ALT = 5

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
else:
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

# Allow to connect, stream, detect, record
connection_allows = [True, True, True, True, True, True]
streaming_enables = [False, False, False, False, False, False]
detection_enables = [False, False, False, False, False, False]
recording_enables = [True, True, True, True, True, True]

DEFAULT_STREAM_SCREEN = "general_screen"  # NOTE: Change between "general_screen" or "stream_screen" or "ovv_screen" or "all"
# NOTE Change for modify recording settings
DEFAULT_STREAM_SIZE = (320, 180)
DEFAULT_STREAM_FPS = 15
FOURCC = "XVID"

# Path settings
"""
Stream source paths:
- video: path to video file (e.g. "path/to/video.mp4")
- rtsp: rtsp://username:password@ip:port
- webcam: /dev/video0, /dev/video1, ...
"""
# NOTE: Change the following values to match the actual stream source
DEFAULT_STREAM_VIDEO_PATHS = [
    f"{ROOT_DIR}/assets/streams/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
]
# Destination paths for recording videos
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    f"{SRC_DIR}/logs/videos/stream_log_uav_{i}_{NOW}.avi" for i in range(1, MAX_UAV_COUNT + 1)
]

os.makedirs(f"{SRC_DIR}/logs/videos", exist_ok=True)

# YOLO settings
model_path = f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt"  # YOLO model path
