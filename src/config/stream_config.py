import os
from datetime import datetime
from pathlib import Path

# cSpell:ignore baudrate, uav, rtl, opencv, cv2, fourcc, rtsp, uet, YOLO, nosignal, XVID

# Do not change
SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent
NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
MAX_UAV_COUNT = 6
#
DEFAULT_STREAM_SCREEN = "general_screen"  # NOTE: Change between "general_screen" or "stream_screen" or "ovv_screen" or "all"
DEFAULT_STREAM_SOURCE = (
    "streams"  # NOTE: Change between "streams" or "rtsp" or "webcam" or "video"
)
DEFAULT_STREAM_SIZE = (320, 180)  # NOTE Change for modify recording settings
DEFAULT_STREAM_FPS = 30
FOURCC = "XVID"

# Path settings
"""
Stream source paths:
- video: path to video file (e.g. "path/to/video.mp4")
- rtsp: rtsp://username:password@ip:port
- webcam: /dev/video0, /dev/video1, ...
"""
# NOTE: Change the following values to match the actual stream source
if DEFAULT_STREAM_SOURCE == "streams":
    DEFAULT_STREAM_VIDEO_PATHS = [
        f"{ROOT_DIR}/assets/streams/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
    ]
elif DEFAULT_STREAM_SOURCE == "video":
    DEFAULT_STREAM_VIDEO_PATHS = [
        f"{ROOT_DIR}/assets/videos/video{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
    ]
elif DEFAULT_STREAM_SOURCE == "rtsp":
    DEFAULT_STREAM_VIDEO_PATHS = [
        f"rtsp://192.168.144.70:8554/main.264",
        f"rtsp://192.168.144.60/video0",
        f"rtsp://192.168.144.60/video1",
        f"rtsp://192.168.144.60/video2",
        f"rtsp://192.168.144.60/video3",
        f"rtsp://192.168.144.60/video4",
    ]
elif DEFAULT_STREAM_SOURCE == "webcam":
    DEFAULT_STREAM_VIDEO_PATHS = [f"/dev/video{i}" for i in range(0, MAX_UAV_COUNT)]

# Destination paths for recording videos
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    f"{SRC_DIR}/logs/videos/stream_log_uav_{i}_{NOW}.avi" for i in range(1, MAX_UAV_COUNT + 1)
]

os.makedirs(f"{SRC_DIR}/logs/videos", exist_ok=True)

# YOLO settings
model_uav_paths = {
    1: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
    2: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
    3: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
    4: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
    5: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
    6: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt",
}  # YOLO model paths
