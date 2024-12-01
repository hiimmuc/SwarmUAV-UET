# cSpell:ignore fourcc dsize interpolation
import time
from collections import defaultdict
from threading import Lock, Thread

import cv2
import numpy as np
import torch
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from ultralytics import YOLO

from .model_utils import *

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# cspell: ignore BUFFERSIZE msleep
class Stream:
    def __init__(self, capture: dict, writer: dict) -> None:
        self.capture_params = capture
        self.writer_params = writer

        self.capture = None
        self.writer = None
        self.connect()

    def connect(self):
        if self.capture is not None:
            self.capture.release()
        if hasattr(self, "writer"):
            if self.writer is not None:
                self.writer.release()

        self.capture = cv2.VideoCapture(self.capture_params["address"])

        # Set capture properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.capture_params["width"]))
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.capture_params["height"]))
        self.capture.set(cv2.CAP_PROP_FPS, int(self.capture_params["fps"]))
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)

        # Set writer properties
        if self.writer_params["enable"]:
            self.writer_frameSize = self.writer_params["frameSize"]
            self.writer = cv2.VideoWriter(
                filename=self.writer_params["filename"],
                fourcc=cv2.VideoWriter_fourcc(*self.writer_params["fourcc"]),
                fps=self.capture.get(cv2.CAP_PROP_FPS),
                frameSize=self.writer_params["frameSize"],
            )

        return self.is_opened()

    def is_opened(self):
        return self.capture.isOpened()

    def is_video(self):
        # Define common video file extensions
        video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
        # Use regex to check for any of the video file extensions in the URL
        return any(
            self.capture_params["address"].lower().endswith(ext) for ext in video_extensions
        )

    def get_fps(self):
        return self.capture.get(cv2.CAP_PROP_FPS)

    def capture_reset(self):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def read(self):
        return self.capture.read()

    def write(self, frame):
        if hasattr(self, "writer"):
            self.writer.write(
                cv2.resize(
                    frame,
                    dsize=self.writer_frameSize,
                    interpolation=cv2.INTER_LINEAR,
                )
            )

    def release(self) -> None:
        self.capture.release()
        if hasattr(self, "writer"):
            self.writer.release()
        return


class StreamThread:
    def __init__(self, stream: Stream):
        self.stream = stream
        self.FPS = 1 / 30
        self.FPS_MS = int(self.FPS * 1000)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            time.sleep(self.FPS)
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


class StreamQtThread(QThread):  # NOTE: slower than using Thread
    change_image_signal = pyqtSignal(np.ndarray, list)

    def __init__(self, uav_index, stream, model_config=None, **kwargs):
        super().__init__()
        self.uav_index = uav_index
        self.track_history = defaultdict(lambda: [])
        self.isRunning = False
        self.stream = stream
        self.model_config = model_config
        self.model = YOLO(model_config["path"]).to(DEVICE)
        print(f">>> Model loaded successfully for UAV-{uav_index} on {DEVICE}!")

    def is_alive(self):
        return self.isRunning

    def run(self):
        self.isRunning = True
        while self.isRunning:
            if not self.stream.connect():
                print(">>> Lost streaming signal, try to reconnect ...")
                self.msleep(1000)
                continue

            while self.stream.is_opened():
                ret, frame = self.stream.read()
                results = [None]
                if ret:
                    if self.model_config["enable"]:
                        results = self.model.track(
                            frame, classes=0, device=DEVICE, persist=True, verbose=False
                        )
                        frame, track_ids, objects = draw_tracking_frame(
                            frame, results, self.track_history, 90
                        )
                        results = [track_ids, objects]

                    self.change_image_signal.emit(frame, [self.uav_index, results])
                    self.msleep(int(1 / self.stream.get_fps() * 1000))
                else:
                    if self.stream.is_video():
                        self.stream.capture_reset()
                    else:
                        print(">>> No frame received, signal may lost ...")
                        self.stream.release()
                        break

                if not self.isRunning:
                    break

            if not self.isRunning:
                break
        self.stream.release()

    def stop(self):
        self.isRunning = False
        self.wait()
