import torch
from ultralytics import YOLO

from config import *

# cspell:ignore ultralytics YOLO

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
MODELS = [YOLO(model_path).to(DEVICE) for _ in range(MAX_UAV_COUNT)]
