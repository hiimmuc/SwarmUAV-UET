import time
from threading import Thread

import cv2
import imutils
import numpy as np
import pyshine as ps
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.mw = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Create labels for 6 videos
        self.labels = []
        for i in range(6):
            label = QtWidgets.QLabel(self.centralwidget)
            label.setText("")
            label.setPixmap(
                QtGui.QPixmap(
                    "/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/pictures/no_signal2.jpg"
                )
            )
            label.setObjectName(f"label_{i+1}")
            self.labels.append(label)
            self.horizontalLayout.addWidget(label)

        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        # Add a button to start the videos
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.startButton.setText("Start Videos")
        self.gridLayout_2.addWidget(self.startButton, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.startButton.clicked.connect(self.start_videos)

    def start_videos(self):
        """
        Start six threads to play videos.
        """
        video_paths = [
            f"/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/videos/cam{i}.mp4"
            for i in range(1, 7)
        ]
        self.threads = []
        for i, path in enumerate(video_paths):
            thread = Thread(target=self.play_video, args=(path, i))
            thread.start()
            self.threads.append(thread)

    def play_video(self, video_path, label_index):
        """
        Play a video from the given path and display it on the specified label.

        Args:
            video_path (str): The path to the video file.
            label_index (int): The index of the label to display the video.
        """
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = imutils.resize(frame, width=200)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.strides[0],
                QImage.Format_RGB888,
            )
            self.labels[label_index].setPixmap(QtGui.QPixmap.fromImage(image))
            time.sleep(0.03)  # Adjust the sleep time to control the frame rate
        cap.release()
