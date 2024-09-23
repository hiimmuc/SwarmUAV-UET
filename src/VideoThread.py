import sys
import time
from threading import Thread  # library for implementing multi-threaded processing

import cv2
import numpy as np
from imutils.video import FPS

# from model.model import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QRunnable, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class VideoThread(QThread, QRunnable):
    change_pixmap_signal = pyqtSignal(int, np.ndarray, list)

    def __init__(self, index=1, source=0, model=None) -> None:
        super().__init__()
        self.run_flag = True
        self.source = source
        self.index = index
        # print(self.source)

        # initialize model here
        self.model = model

        print(f"[INFO] VideoThread for UAV {index} initialized")

    def run(self) -> None:
        try:
            print(f"[INFO] Start recording for UAV {self.index}...")
            self.cap = cv2.VideoCapture(self.source)
            self.fps = FPS().start()

            while self.run_flag:
                ret, frame = self.cap.read()
                print(frame.shape)
                if not ret:
                    # Set video position to the first frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                # if self.model is not None:
                #     # detect
                #     bBoxes, _ = self.model.detect(frame, show=False)
                #     pass
                if ret:
                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.change_pixmap_signal.emit(self.index, frame, [1, 2, 3])
                    self.fps.update()

            self.fps.stop()

            print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        except Exception as e:
            print(repr(e))

    def stop(self) -> None:
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.cap.release()
        self.wait()


class win(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setGeometry(250, 80, 800, 600)
        self.setWindowTitle("camera")
        # self.cap = cv2.VideoCapture(0)
        self.video_thread = VideoThread(
            1,
            "/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/videos/cam1.mp4",
            None,
        )
        self.video_thread.change_pixmap_signal.connect(self.refresh)

        self.videoFrame = QLabel("VideoCapture")
        # add buttons to start and stop the program
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.clicked.connect(self.start_program)
        self.stop_button.clicked.connect(self.stop_program)
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.videoFrame)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_program(self):
        self.video_thread.start()

    def stop_program(self):
        self.video_thread.stop()

    @pyqtSlot(int, np.ndarray, list)
    def refresh(self, id, img, bBoxes):
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width = img.shape[:2]
            print(f"height: {height}, width: {width}")
            img = QPixmap.fromImage(QImage(img, width, height, QImage.Format_RGB888))
            self.videoFrame.setPixmap(img)
        except TypeError:
            print("No Frame")


if __name__ == "__main__":
    # # # initializing and starting multi-threaded webcam capture input stream
    # # # stream_id = 0 is for primary camera
    # webcam_stream = WebcamStream(stream_id=0)
    # webcam_stream.start()
    # # processing frames in input stream
    # num_frames_processed = 0
    # start = time.time()
    # while True:
    #     if webcam_stream.stopped is True:
    #         break
    #     else:
    #         frame = webcam_stream.read()
    #     # adding a delay for simulating time taken for processing a frame
    #     delay = 0.03  # delay value in seconds. so, delay=1 is equivalent to 1 second
    #     time.sleep(delay)
    #     num_frames_processed += 1
    #     cv2.imshow("frame", frame)
    #     key = cv2.waitKey(1)
    #     if key == ord("q"):
    #         break

    # end = time.time()
    # webcam_stream.stop()  # stop the webcam stream
    # # printing time elapsed and fps
    # elapsed = end - start
    # fps = num_frames_processed / elapsed
    # print(
    #     "FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(
    #         fps, elapsed, num_frames_processed
    #     )
    # )
    # # closing all windows
    # cv2.destroyAllWindows()

    #
    # app = QApplication(sys.argv)
    # win = win()
    # win.show()
    # sys.exit(app.exec_())
    pass
