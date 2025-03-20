"""
Stream Configuration Module

This module defines configuration settings for video streams including sources,
recording parameters, and detection models for UAV applications.
"""

import os
from datetime import datetime
from pathlib import Path

import torch

from .uav_config import MAX_UAV_COUNT

# cSpell:ignore baudrate, uav, yolov, rtl, opencv, cv2, fourcc, rtsp, uet, YOLO, nosignal, XVID

# Device configuration for model inference
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Base paths (do not change)
SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent
NOW = datetime.now().strftime("%y-%m-%d_%H-%M-%S")

# Stream display configuration
DEFAULT_STREAM_SCREEN = "general_screen"  # Options: "general_screen", "stream_screen", "ovv_screen", "all"

# Stream source configuration
DEFAULT_STREAM_SOURCE = "videos"  # Options: "streams", "rtsp", "webcam", "videos"
DEFAULT_STREAM_SIZE = (320, 180)  # Recording resolution
DEFAULT_STREAM_FPS = 30           # Frame rate for streaming and recording
FOURCC = "XVID"                   # Video codec for recording

# Screen size configuration for different views (for display)
screen_sizes = {
    "general_screen": (640, 360),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}

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

# Stream source paths based on selected source type
"""
Stream source paths:
- videos: Path to video files (e.g., "/path/to/video.mp4")
- rtsp: RTSP URL (e.g., "rtsp://username:password@ip:port")
- webcam: Device path (e.g., "/dev/video0", "/dev/video1", etc.)
- streams: Path to streaming files
"""

# Configure stream paths based on selected source type
if DEFAULT_STREAM_SOURCE == "streams":
    DEFAULT_STREAM_VIDEO_PATHS = [
        f"{ROOT_DIR}/assets/streams/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
    ]
elif DEFAULT_STREAM_SOURCE == "videos":
    DEFAULT_STREAM_VIDEO_PATHS = [
        f"{ROOT_DIR}/assets/videos/cam{i}.mp4" for i in range(1, MAX_UAV_COUNT + 1)
    ]
elif DEFAULT_STREAM_SOURCE == "rtsp":
    DEFAULT_STREAM_VIDEO_PATHS = [
        "rtsp://192.168.144.70:8554/main.264",
        "rtsp://192.168.144.60/video0",
        "rtsp://192.168.144.60/video1",
        "rtsp://192.168.144.60/video2",
        "rtsp://192.168.144.60/video3",
        "rtsp://192.168.144.60/video4",
    ]
elif DEFAULT_STREAM_SOURCE == "webcam":
    DEFAULT_STREAM_VIDEO_PATHS = [f"/dev/video{i}" for i in range(0, MAX_UAV_COUNT)]
else:
    DEFAULT_STREAM_VIDEO_PATHS = []

# Destination paths for recording videos
DEFAULT_STREAM_VIDEO_LOG_PATHS = [
    f"{SRC_DIR}/logs/recordings/stream_log_uav_{i}_{NOW}.avi" 
    for i in range(1, MAX_UAV_COUNT + 1)
]

# Create necessary directories
os.makedirs(f"{SRC_DIR}/logs/images", exist_ok=True)
os.makedirs(f"{SRC_DIR}/logs/recordings", exist_ok=True)
os.makedirs(f"{SRC_DIR}/logs/stream_properties", exist_ok=True)

# YOLO model paths for each UAV
model_uav_paths = {
    i: f"{SRC_DIR}/model/checkpoints/YOLO/yolov8n.pt"
    for i in range(1, MAX_UAV_COUNT + 1)
}

# Configuration validation
def validate_config():
    """
    Validate configuration settings and return any issues found.
    
    Returns:
        List of warning messages for potential configuration issues
    """
    warnings = []
    
    # Check if stream source exists
    if DEFAULT_STREAM_SOURCE in ["videos", "streams"]:
        for path in DEFAULT_STREAM_VIDEO_PATHS:
            if not os.path.exists(path):
                warnings.append(f"Warning: Stream source file not found: {path}")
    
    # Check if YOLO model files exist
    for uav_index, model_path in model_uav_paths.items():
        if not os.path.exists(model_path):
            warnings.append(f"Warning: YOLO model file not found for UAV {uav_index}: {model_path}")
    
    return warnings


# Run validation when module is imported
config_warnings = validate_config()
for warning in config_warnings:
    print(warning)