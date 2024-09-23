import sys

import cv2
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Create a label to display the video frames
        self.label = QLabel(self)

        # Create a layout to hold the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Load the video file (Change the path to the correct video file)
        self.cap = cv2.VideoCapture(
            "/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/videos/cam1.mp4"
        )

        # Create a QTimer object
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Start the timer, with a 30 ms interval (about 33 FPS)
        self.timer.start(30)

    @pyqtSlot()
    def update_frame(self):
        # Read the next frame from the video
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to QImage for display in QLabel
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Display the frame in the QLabel
            self.label.setPixmap(QPixmap.fromImage(q_image))
        else:
            # Restart the video if it finishes
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def closeEvent(self, event):
        # Release the video capture object when the window is closed
        self.cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setWindowTitle("Video Player")
    player.setGeometry(100, 100, 800, 600)
    player.show()
    sys.exit(app.exec_())
