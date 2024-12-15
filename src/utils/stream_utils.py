# cSpell:ignore fourcc dsize interpolation
import time
from collections import defaultdict
from threading import Lock, Thread
from typing import Any, Dict

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

from config.stream_config import *

from .model_utils import *


# cspell: ignore BUFFERSIZE msleep ndarray videowriter NSTRIPES FRAMEBYTES
class Stream:
    def __init__(self, capture: dict, writer: dict) -> None:
        self.capture_params = capture
        self.writer_params = writer

        self.capture = None
        self.writer = None
        self.connect()

    def connect(self) -> bool:
        # Release previous capture and writer
        try:
            self.release()
        except Exception as e:
            print(f"Error: {repr(e)}")
            pass

        self.capture = cv2.VideoCapture(self.capture_params["address"].strip())

        # Set capture properties
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.capture_params["width"]))
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.capture_params["height"]))
        # self.capture.set(cv2.CAP_PROP_FPS, int(self.capture_params["fps"]))
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Set writer properties
        if self.writer_params["enable"]:
            self.writer_frameSize = self.writer_params["frameSize"]
            self.writer = cv2.VideoWriter(
                filename=self.writer_params["filename"],
                fourcc=cv2.VideoWriter_fourcc(*self.writer_params["fourcc"]),
                fps=self.capture.get(cv2.CAP_PROP_FPS),
                frameSize=self.writer_params["frameSize"],
            )

        self.export_properties()
        return self.is_capture_opened()

    def is_capture_opened(self):
        return self.capture.isOpened()

    def is_writer_opened(self):
        if hasattr(self, "writer"):
            return self.writer.isOpened()
        else:
            return False

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

    def capture_reset(self):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def release(self) -> None:
        if self.capture is not None:
            self.capture.release()
        if hasattr(self, "writer"):
            if self.writer is not None:
                self.writer.release()
        return

    def is_video(self):
        # Define common video file extensions
        video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
        # Use regex to check for any of the video file extensions in the URL
        return any(
            self.capture_params["address"].lower().endswith(ext) for ext in video_extensions
        )

    def get_fps(self):
        return self.capture.get(cv2.CAP_PROP_FPS)

    def export_properties(self):
        with open(
            f"{SRC_DIR}/logs/stream_properties/stream_{self.capture_params['index']}.log",
            "w",
        ) as f:
            f.write("Capture Properties\n")
            if self.is_capture_opened():
                f.write(f"Address: {self.capture_params['address']}\n")
                f.write(
                    "CV_CAP_PROP_FRAME_WIDTH: '{}'\n".format(
                        self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
                    )
                )
                f.write(
                    "CV_CAP_PROP_FRAME_HEIGHT: '{}'\n".format(
                        self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    )
                )
                f.write("CV_CAP_PROP_FPS: '{}'\n".format(self.capture.get(cv2.CAP_PROP_FPS)))
                f.write(
                    "CV_CAP_PROP_BUFFERSIZE: '{}'\n".format(
                        self.capture.get(cv2.CAP_PROP_BUFFERSIZE)
                    )
                )
                f.write("CAP_PROP_MODE: '{}'\n".format(self.capture.get(cv2.CAP_PROP_MODE)))
                f.write(
                    "CAP_PROP_CODEC_PIXEL_FORMAT: '{}'\n".format(
                        self.capture.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT)
                    )
                )
                f.write("CAP_PROP_BITRATE: '{}'\n".format(self.capture.get(cv2.CAP_PROP_BITRATE)))
                f.write("CAP_PROP_BACKEND: '{}'\n".format(self.capture.get(cv2.CAP_PROP_BACKEND)))
                if self.is_video():
                    f.write(
                        "CAP_PROP_POS_MSEC: '{}'\n".format(self.capture.get(cv2.CAP_PROP_POS_MSEC))
                    )
                    f.write(
                        "CAP_PROP_POS_FRAMES: '{}'\n".format(
                            self.capture.get(cv2.CAP_PROP_POS_FRAMES)
                        )
                    )
                    f.write(
                        "CAP_PROP_POS_AVI_RATIO: '{}'\n".format(
                            self.capture.get(cv2.CAP_PROP_POS_AVI_RATIO)
                        )
                    )
                    f.write(
                        "CAP_PROP_FRAME_COUNT: '{}'\n".format(
                            self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
                        )
                    )
                    f.write(
                        "CAP_PROP_FOURCC: '{}'\n".format(self.capture.get(cv2.CAP_PROP_FOURCC))
                    )
                else:
                    f.write(
                        "CAP_PROP_BRIGHTNESS: '{}'\n".format(
                            self.capture.get(cv2.CAP_PROP_BRIGHTNESS)
                        )
                    )
                    f.write(
                        "CAP_PROP_CONTRAST: '{}'\n".format(self.capture.get(cv2.CAP_PROP_CONTRAST))
                    )
                    f.write(
                        "CAP_PROP_SATURATION: '{}'\n".format(
                            self.capture.get(cv2.CAP_PROP_SATURATION)
                        )
                    )
                    f.write("CAP_PROP_HUE: '{}'\n".format(self.capture.get(cv2.CAP_PROP_HUE)))
                    f.write("CAP_PROP_GAIN: '{}'\n".format(self.capture.get(cv2.CAP_PROP_GAIN)))
                    f.write(
                        "CAP_PROP_EXPOSURE: '{}'\n".format(self.capture.get(cv2.CAP_PROP_EXPOSURE))
                    )

            f.write("\nWriter Properties\n")
            if self.is_writer_opened():
                f.write(f"Filename: {self.writer_params['filename']}\n")
                f.write(
                    "VIDEOWRITER_PROP_QUALITY: '{}'\n".format(
                        self.writer.get(cv2.VIDEOWRITER_PROP_QUALITY)
                    )
                )
                f.write(
                    "VIDEOWRITER_PROP_FRAMEBYTES: '{}'\n".format(
                        self.writer.get(cv2.VIDEOWRITER_PROP_FRAMEBYTES)
                    )
                )
                f.write(
                    "VIDEOWRITER_PROP_NSTRIPES: '{}'\n".format(
                        self.writer.get(cv2.VIDEOWRITER_PROP_NSTRIPES)
                    )
                )
        return


class StreamQtThread(QThread):  # NOTE: slower than using Thread
    change_image_signal = pyqtSignal(np.ndarray, np.ndarray, list)

    def __init__(self, uav_index: int, stream: Stream, detection_model: Any, **kwargs):
        super().__init__()
        self.isRunning = False
        self.track_history = defaultdict(lambda: [])

        self.stream = stream
        self.uav_index = uav_index
        self.model = detection_model

    def is_alive(self):
        return self.isRunning

    def run(self):
        self.isRunning = True
        while self.isRunning:
            if not self.stream.connect():
                print(">>> Lost streaming signal, try to reconnect ...")
                self.msleep(1000)
                continue

            while self.stream.is_capture_opened():
                ret, frame = self.stream.read()
                annotated_frame = np.zeros_like(frame)
                elapsed_time = 0
                results = [None]
                if ret:
                    processing_start = time.time()
                    if self.model is not None:
                        results = self.model.track(
                            source=frame,
                            classes=0,  # 0: person
                            conf=0.5,
                            iou=0.5,
                            device=DEVICE,
                            persist=True,
                            verbose=False,
                        )
                        annotated_frame, track_ids, objects = draw_tracking_frame(
                            frame, results, self.track_history, int(self.stream.get_fps()) * 3
                        )
                        results = [track_ids, objects]
                    else:
                        annotated_frame = frame
                    processing_end = time.time()
                    elapsed_time = processing_end - processing_start
                    # write to saved video
                    if self.stream.is_writer_opened():
                        self.stream.write(annotated_frame)
                    # emit signal to update GUI
                    self.change_image_signal.emit(
                        frame,
                        annotated_frame,
                        [self.uav_index, int(self.stream.get_fps()), results],
                    )
                    # delay to match the FPS
                    adaptive_delay = max(self.stream.get_fps(), elapsed_time)
                    self.msleep(int(1000 * 1 / adaptive_delay))
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


# ! Deprecated
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
