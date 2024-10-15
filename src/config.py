from datetime import datetime
from pathlib import Path

import torch

SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

MODE = "simulation"  # "simulation" or "real"

# UAV settings
MAX_UAV_COUNT = 6

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

DEFAULT_PROTOCOL = "udp"
DEFAULT_SERVER_HOST = ""
DEFAULT_SERVER_PORT = 14541
DEFAULT_CLIENT_PORT = 50060

if MODE == "simulation":
    PROTOCOLS = [DEFAULT_PROTOCOL] * MAX_UAV_COUNT
    SERVER_HOSTS = [DEFAULT_SERVER_HOST] * MAX_UAV_COUNT
    SERVER_PORTS = [DEFAULT_SERVER_PORT + i for i in range(MAX_UAV_COUNT)]
    CLIENT_PORTS = [DEFAULT_CLIENT_PORT + i for i in range(MAX_UAV_COUNT)]
else:
    PROTOCOLS = ["serial"] + [DEFAULT_PROTOCOL] * (MAX_UAV_COUNT - 1)
    SERVER_HOSTS = ["/dev/ttyACM0"] + [DEFAULT_SERVER_HOST] * (MAX_UAV_COUNT - 1)
    SERVER_PORTS = [57600] + [DEFAULT_SERVER_PORT + i for i in range(1, MAX_UAV_COUNT)]
    CLIENT_PORTS = [50060] + [DEFAULT_CLIENT_PORT + i for i in range(1, MAX_UAV_COUNT)]

SYSTEMS_ADDRESSES = [
    f"{proto}://{server_host}:{server_port}"
    for (proto, server_host, server_port) in zip(PROTOCOLS, SERVER_HOSTS, SERVER_PORTS)
]

connection_allows = [True, True, False, False, False, False]
streaming_enables = [True, False, False, False, False, False]
detection_enables = [True, False, False, False, False, False]

screen_sizes = {
    "general_screen": (592, 333),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}

DEFAULT_STREAM_SIZE = (480, 270)
DEFAULT_STREAM_SCREEN = "general_screen"

# Path settings
"""
Stream source paths:
- video: path to video file (e.g. "path/to/video.mp4")
- rtsp: rtsp://username:password@ip:port
- webcam: /dev/video0, /dev/video1, ...
"""
DEFAULT_STREAM_VIDEO_PATHS = [
    f"{ROOT_DIR}/assets/videos/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
]
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    f"{SRC_DIR}/logs/videos/stream_log_uav_{i}_{NOW}.avi" for i in range(1, MAX_UAV_COUNT + 1)
]

INIT_LON = 8.545594
INIT_LAT = 47.397823

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
    k: f"{ROOT_DIR}/assets/pictures/resized/nosignal_{h}x{w}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/pause_screen_{h}x{w}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths["all"] = f"{ROOT_DIR}/assets/pictures/pause_screen.jpg"

map_html_path = f"file://{ROOT_DIR}/assets/map.html"

model_path = f"{SRC_DIR}/model/checkpoints/YOLO/yolov9t.pt"
gps_log_paths = [
    f"{SRC_DIR}/logs/gps/gps_log_uav_{i}_{NOW}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
plans_log_dir = f"{SRC_DIR}/logs/points/"
