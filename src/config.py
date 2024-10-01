from datetime import datetime
from pathlib import Path

import torch

SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
DEFAULT_STREAM_SIZE = (640, 360)
DEFAULT_STREAM_SCREEN = "general_screen"

# UAV settings
MAX_UAV_COUNT = 6

PROTO = "udp"
SERVER_HOST = ""
DEFAULT_PORT = 50060
DEFAULT_BIND_PORT = 14541

connection_allows = [True, True, True, True, True, True]
streaming_enables = [True, False, False, False, False, False]

screen_sizes = {
    "general_screen": (592, 333),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}

# Path settings
DEFAULT_STREAM_VIDEO_PATHS = [
    f"{ROOT_DIR}/assets/videos/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
]
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    f"{SRC_DIR}/logs/videos/stream_log_uav_{i}_{NOW}.avi" for i in range(1, MAX_UAV_COUNT + 1)
]

logo1_path = f"{ROOT_DIR}/assets/icons/logo1.png"
logo2_path = f"{ROOT_DIR}/assets/icons/logoUET.png"
app_icon_path = f"{ROOT_DIR}/assets/icons/app.png"
noSignal_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/nosignal_{h}x{w}.jpg"
    for k, (w, h) in screen_sizes.items()
}
pause_img_paths = {
    k: f"{ROOT_DIR}/assets/pictures/resized/pause_screen_{h}x{w}.jpg"
    for k, (w, h) in screen_sizes.items()
}
map_html_path = f"file://{ROOT_DIR}/assets/map.html"
model_path = f"{SRC_DIR}/model/checkpoints/yolov8n.pt"
gps_log_paths = [
    f"{SRC_DIR}/logs/gps/gps_log_uav_{i}_{NOW}.txt" for i in range(1, MAX_UAV_COUNT + 1)
]
plans_log_dir = f"{SRC_DIR}/logs/points/"
