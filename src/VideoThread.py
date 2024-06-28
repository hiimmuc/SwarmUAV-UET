"""simple edition, just display the webcam"""
# from imutils. import FPS
# from facedetect_yolo import Yolov4
from threading import Thread
import sys

import cv2
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

import time


class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True


class VideoShow:
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == 27:
                self.stopped = True

    def stop(self):
        self.stopped = True


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        # self.data = Data()
        self.model = self.data.model

    def run(self):
        # capture from web cam
        # cap = cv2.VideoCapture(0)
        video_cap = VideoGet().start()
        delay = 0
        while self._run_flag:
            if video_cap.stopped:
                video_cap.stop()
                break
            frame = video_cap.frame
            output_img, value = self.model.detector(frame, 0.5, 0.4, delay)

            self.change_pixmap_signal.emit(output_img)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
