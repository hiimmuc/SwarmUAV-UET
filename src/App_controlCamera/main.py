from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys
from interface import Ui_MainWindow
from control import Ui_SETTING
from gimbal import Ui_Form
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import asyncio
from asyncqt import QEventLoop, asyncSlot

# thu vien sdk cua camera
from siyi_sdk import SIYISDK
import os
from time import sleep
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.

#connect camera 
cam = SIYISDK(server_ip="192.168.144.25", port=37260)


# lop chinh cam
class CamAngle:
    def __init__(self):
        self.yaw = 0
        self.pitch = 0
    
    def addYaw(self, dy):
        self.yaw += dy
        if self.yaw >135:
            self.yaw = 135
        if self.yaw <-135:
            self.yaw = -135

    def addPitch(self, dp):
        self.pitch += dp
        if self.pitch >25:
            self.pitch = 25
        if self.pitch <-90:
            self.pitch = -90
    def zeroYaw(self):
        self.yaw = 0

    def zeroPitch(self):
        self.pitch = 0
cam_angle = CamAngle()
class MainWindow():
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)

        # stream video 
        self.start_capture_video

        # get camera version
        self.Firmware


        # nut bam cac chuc nang
        self.uic.settingButton.clicked.connect(self.open_Setting)
        self.uic.controlButton.clicked.connect(self.open_Control)
        self.uic.pushButton_7.clicked.connect(self.start_capture_video)
        self.uic.photoButton.clicked.connect(self.makePhoto)
        self.uic.recordButton.clicked.connect(self.Record)
        self.uic.zoomInButton.clicked.connect(self.Zoom_in)
        self.uic.zoomOutButton.clicked.connect(self.Zoom_out)
        self.uic.zoomX.clicked.connect(self.ZoomX)

        self.thread = {}

        #check connection 
        if not cam.connect():
            print("No connection ")
            self.uic.plainTextEdit.appendPlainText("-No connection")
            
        else:
            self.uic.plainTextEdit.appendPlainText("-Connection successfull")
#---------------------------------------------------------------------------------------
# Photo from camera
    def makePhoto(self):
        global cam
        val =  cam.requestPhoto()
        print("-Taking the photo")
        self.uic.plainTextEdit.appendPlainText("- Taking the photo")
        if(cam.requestPhoto() ==  True):
            print("-Successful taking the photo")
            self.uic.plainTextEdit.appendPlainText("- Successful taking the photo")
        return None
#---------------------------------------------------------------------------------------
    def Record(self):
        global cam
        #if (cam.getRecordingState()<0):
        print("Toggle recording")
        self.uic.plainTextEdit.appendPlainText("Toggle recording")
        cam.requestRecording()
        sleep(5)
        if (cam.getRecordingState()<0):
            print("Toggle recording")
            self.uic.plainTextEdit.appendPlainText("Toggle recording")
            #await 
            cam.requestRecording()
            sleep(5)
        if (cam.getRecordingState()==cam._record_msg.TF_EMPTY):
            print("TF card lsot is empty")
            self.uic.plainTextEdit.appendPlainText("TF card lsot is empty")

        if (cam.getRecordingState()==cam._record_msg.ON):
            print("Recording is ON. Sending requesdt to stop recording")
            self.uic.plainTextEdit.appendPlainText("Recording is ON. Sending requesdt to stop recording")
            cam.requestRecording()
            sleep(2)

        print("Recording state: ", cam.getRecordingState())
        self.uic.plainTextEdit.appendPlainText("")
#-----------------------------------------------------------------------------------------
    def Zoom_in(self):
        val = cam.requestZoomIn()
        sleep(1)
        val =  cam.requestZoomHold()
        sleep(1)
        print("Zoom level: ", cam.getZoomLevel())
        self.uic.plainTextEdit.appendPlainText("Zoom level: ", cam.getZoomLevel())

#--------------------------------------------------------------------------------------------
    def Zoom_out(self):
        val =  cam.requestZoomOut()
        sleep(1)
        val =  cam.requestZoomHold()
        sleep(1)
        print("Zoom level: ", cam.getZoomLevel())
        self.uic.plainTextEdit.appendPlainText("Zoom level:",cam.getZoomLevel())

#--------------------------------------------------------------------------------------------
    def ZoomX(self):
        value = float(self.uic.plainTextEdit_2.toPlainText())
        val =  cam.requestAbsoluteZoom(value)
        sleep(1)
        print("Zoom level: ", cam.getZoomLevel())
        self.uic.plainTextEdit.appendPlainText("Zoom level:",cam.getZoomLevel())
#---------------------------------------------------------------------------------------
    def control_Center(self):
        #val = cam.requestCenterGimbal()
        #sleep(1)
        #print("Centering gimbal: ", cam.getFunctionFeedback())
        #self.uic.plainTextEdit.appendPlainText("Centering gimbal: ", cam.getFunctionFeedback())
        cam_angle.zeroYaw()
        cam_angle.zeroPitch()
        cam.requestAbsolutePosition(cam_angle.yaw, cam_angle.pitch)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())
#---------------------------------------------------------------------------------------------
    def control_Up(self):
        val =  cam_angle.addPitch(10)
        sleep(1)
        val = cam.requestAbsolutePosition(cam_angle.yaw, cam_angle.pitch)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())
#----------------------------------------------------------------------------------------------
    def control_Down(self):
        val =cam_angle.addPitch(-10)
        sleep(1)
        val = cam.requestAbsolutePosition(cam_angle.yaw, cam_angle.pitch)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())

#----------------------------------------------------------------------------------------------
    def control_Left(self):
        val = cam_angle.addYaw(10)
        sleep(1)
        val = cam.requestAbsolutePosition(cam_angle.yaw, cam_angle.pitch)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())

#----------------------------------------------------------------------------------------------
    def control_Right(self):
        val = cam_angle.addYaw(-10)
        sleep(1)
        val = cam.requestAbsolutePosition(cam_angle.yaw, cam_angle.pitch)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())

#----------------------------------------------------------------------------------------------
    def control_Straigh(self):
        val = cam.requestAbsolutePosition(0,-90)
        # cam.setGimbalRotation(0,10)
        print("Attitude (yaw,pitch,roll) eg:", cam.getAttitude())
#-----------------------------------------------------------------------------------------------
    def follow_Mode(self):
        val = cam.requestFollowMode()
        print("Current motion mode: ", cam._motionMode_msg.mode)

#-----------------------------------------------------------------------------------------------
    def fpv_Mode(self):
        val = cam.requestFPVMode()
        print("Current motion mode: ", cam._motionMode_msg.mode)

#-----------------------------------------------------------------------------------------------
    def lock_Mode(self):
        val = cam.requestLockMode()
        print("Current motion mode: ", cam._motionMode_msg.mode)

#-----------------------------------------------------------------------------------------------
    def Firmware(self):
        cam.requestFirmwareVersion()
        print("Camera Firmware version: ", cam.getFirmwareVersion())
        self.uic1.Gimbal_ver.setText("v",cam._fw_msg.gimbal_firmware_ver)
        self.uic1.Zoom_ver.setText("v",cam._fw_msg.zoom_firmware_ver)
#----------------------------------------------------------------------------------------------
    def show(self):
        self.main_win.show()
#----------------------------------------------------------------------------------------------

    # open window setting mode and version
    def open_Setting(self):
        self.Setting_window = QtWidgets.QMainWindow()
        self.uic1 = Ui_SETTING()
        self.uic1.setupUi(self.Setting_window)
        self.Setting_window.show()
        self.uic1.followButton.clicked.connect(self.follow_Mode)
        self.uic1.fpvButton.clicked.connect(self.fpv_Mode)
        self.uic1.lockButton.clicked.connect(self.lock_Mode)

    #open window control gimbal
    def open_Control(self):
        self.Control_window = QtWidgets.QMainWindow()
        self.uic2 = Ui_Form()
        self.uic2.setupUi(self.Control_window)
        self.Control_window.show()
        #nut bam dieu khien camera
        self.uic2.CENTER.clicked.connect(self.control_Center)
        self.uic2.UP.clicked.connect(self.control_Up)
        self.uic2.DOWN.clicked.connect(self.control_Down)
        self.uic2.LEFT.clicked.connect(self.control_Left)
        self.uic2.RIGHT.clicked.connect(self.control_Right)
        self.uic2.Straigh.clicked.connect(self.control_Straigh)

    def start_capture_video(self):
        self.thread[1] = capture_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label_2.setPixmap(qt_img)
        self.uic.label_2.setScaledContents(True)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 420, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def closeEvent(self, event):
        self.stop_capture_video()
    def stop_capture_video(self):
        self.thread[1].stop()

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(capture_video, self).__init__()

    def run(self):
        cap = cv2.VideoCapture('1')  # '/home/lamvu/Downloads/140111-774507949_tiny.mp4''rtsp://192.168.144.25:8554/main.264'
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.signal.emit(cv_img)
    def stop(self):
        print("stop threading", self.index)
        self.terminate()


# Create a Qt widget, which will be our window.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())