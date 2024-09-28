# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'process.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#
# Subscribe to PyShine Youtube channel for more detail!

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
        MainWindow.resize(498, 522)
        self.mw = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(
            QtGui.QPixmap(
                "/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/pictures/no_signal2.jpg"
            )
        )
        # self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # adding another label for second video
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setText("")
        self.label_4.setPixmap(
            QtGui.QPixmap(
                "/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/pictures/no_signal2.jpg"
            )
        )
        # self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.label_4)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridLayout.addWidget(self.verticalSlider, 0, 0, 1, 1)
        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.gridLayout.addWidget(self.verticalSlider_2, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            313, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.verticalSlider.valueChanged["int"].connect(self.brightness_value)
        self.verticalSlider_2.valueChanged["int"].connect(self.blur_value)

        self.th = {}
        self.pushButton_2.clicked.connect(self.run_threads)

        self.pushButton.clicked.connect(self.savePhoto)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Added code here
        self.filename = (
            "Snapshot " + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + ".png"
        )  # Will hold the image address location
        self.tmps = [None, None]  # Will hold the temporary image for display

        self.brightness_value_now = 0  # Updated brightness value
        self.blur_value_now = 0  # Updated blur value
        self.fps = 0

        self.started = [False, False]
        self.labels = [self.label, self.label_4]

    def run_threads(self):
        for i in range(2):
            self.th[i] = Thread(target=self.loadImage, args=(i,), name=f"Thread-{i}")
            self.th[i].start()
        # self.th[self.mw.sender().objectName()] = Thread(
        #     target=self.play_videos, args=(self.mw.sender().objectName(),)
        # )
        # self.th[self.mw.sender().objectName()].start()

    def loadImage(self, index):
        """This function will load the camera device, obtain the image
        and set it to label using the setPhoto function
        """

        if self.started[index]:
            self.started[index] = False
            self.pushButton_2.setText("Start")
        else:
            self.started[index] = True
            self.pushButton_2.setText("Stop")

        vid = cv2.VideoCapture(
            f"/media/phuongnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/assets/videos/cam{index+1}.mp4"
        )

        cnt = 0
        frames_to_count = 20
        st = 0
        fps = 0

        while vid.isOpened():
            # QtWidgets.QApplication.processEvents()
            ret, image = vid.read()
            if ret:
                image = imutils.resize(image, height=480)

                if cnt == frames_to_count:
                    try:  # To avoid divide by 0 we put it in try except
                        print(frames_to_count / (time.time() - st), "FPS")
                        fps = round(frames_to_count / (time.time() - st))
                        st = time.time()
                        cnt = 0
                    except:
                        pass

                cnt += 1

                self.update(image, self.labels[index], fps)
            else:
                vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # key = cv2.waitKey(1) & 0xFF
            if self.started[index] == False:
                break
                print("Loop break")

    def setPhoto(self, image, label):
        """This function will take image input and resize it
        only for display purpose and convert it to QImage
        to set at the label.
        """
        if label is self.label:
            self.tmps[0] = image
        if label is self.label_4:
            self.tmps[1] = image
        image = imutils.resize(image, width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            frame,
            frame.shape[1],
            frame.shape[0],
            frame.strides[0],
            QImage.Format_RGB888,
        )

        label.setPixmap(QtGui.QPixmap.fromImage(image))
        # label.setScaledContents(True)

    def brightness_value(self, value):
        """This function will take value from the slider
        for the brightness from 0 to 99
        """
        self.brightness_value_now = value
        print("Brightness: ", value)
        # self.update()

    def blur_value(self, value):
        """This function will take value from the slider
        for the blur from 0 to 99"""
        self.blur_value_now = value
        print("Blur: ", value)
        # self.update()

    def changeBrightness(self, img, value):
        """This function will take an image (img) and the brightness
        value. It will perform the brightness change using OpenCv
        and after split, will merge the img and return it.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def changeBlur(self, img, value):
        """This function will take the img image and blur values as inputs.
        After perform blur operation using opencv function, it returns
        the image img.
        """
        kernel_size = (value + 1, value + 1)  # +1 is to avoid 0
        img = cv2.blur(img, kernel_size)
        return img

    def update(self, image, label, fps):
        """This function will update the photo according to the
        current values of blur and brightness and set it to photo label.
        """
        img = self.changeBrightness(image, self.brightness_value_now)
        img = self.changeBlur(img, self.blur_value_now)

        # Here we add display text to the image
        text = "FPS: " + str(fps)
        img = ps.putBText(
            img,
            text,
            text_offset_x=20,
            text_offset_y=30,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(10, 20, 222),
            text_RGB=(255, 255, 255),
        )
        text = str(time.strftime("%H:%M %p"))
        img = ps.putBText(
            img,
            text,
            text_offset_x=image.shape[1] - 180,
            text_offset_y=30,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(228, 20, 222),
            text_RGB=(255, 255, 255),
        )
        text = f"Brightness: {self.brightness_value_now}"
        img = ps.putBText(
            img,
            text,
            text_offset_x=80,
            text_offset_y=425,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(20, 210, 4),
            text_RGB=(255, 255, 255),
        )
        text = f"Blur: {self.blur_value_now}: "
        img = ps.putBText(
            img,
            text,
            text_offset_x=image.shape[1] - 200,
            text_offset_y=425,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(210, 20, 4),
            text_RGB=(255, 255, 255),
        )

        self.setPhoto(img, label)

    def savePhoto(self):
        """This function will save the image"""
        self.filename = (
            "Snapshot v1" + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + ".png"
        )
        self.filename2 = (
            "Snapshot v2" + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + ".png"
        )
        if self.tmp is not None:
            cv2.imwrite(self.filename, self.tmp)
            print("Image saved as:", self.filename)
        if self.tmp2 is not None:
            cv2.imwrite(self.filename2, self.tmp2)
            print("Image saved as:", self.filename2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyShine video process"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))

        self.label_2.setText(_translate("MainWindow", "Brightness"))
        self.label_3.setText(_translate("MainWindow", "Blur"))
        self.pushButton.setText(_translate("MainWindow", "Take picture"))


# Subscribe to PyShine Youtube channel for more detail!

# WEBSITE: www.pyshine.com


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
