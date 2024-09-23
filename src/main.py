# !/usr/bin/env python3

import asyncio
import math
import os
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from asyncqt import QEventLoop, asyncSlot
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import QPropertyAnimation, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QSizeGrip,
)

# from VideoThread import *
from UI.ui_interface import *

parent_dir = Path(__file__).parent

# Gán địa chỉ port kết nối cho từng drone thông qua thư viện mavsdk
drone_1 = System(mavsdk_server_address="localhost", port=50060)
drone_2 = System(mavsdk_server_address="localhost", port=50061)
drone_3 = System(mavsdk_server_address="localhost", port=50062)
drone_4 = System(mavsdk_server_address="localhost", port=50063)
drone_5 = System(mavsdk_server_address="localhost", port=50064)
drone_6 = System(mavsdk_server_address="localhost", port=50065)

video_1 = "xx1.mp4"
video_2 = "xx2.mp4"
video_3 = "xx3.mp4"
video_4 = "xx4.mp4"
video_5 = "xx5.mp4"
video_6 = "xx6.mp4"


# Class giao diện MainWindow, nó kế thừa từ lớp (QMainWindown)>> MainWindow là một lớp con của QMainWindown và kế thừa các thuộc tính và phương thức từ QMainWindown.
class MainWindow(QMainWindow):
    """Khởi tạo"""

    def __init__(self):  # Định nghĩa phương thức __init__
        QMainWindow.__init__(self)
        # Tạo một đối tượng của lớp Ui_MainWindow và gán nó cho thuộc tính ui của đối tượng hiện tại
        self.ui = Ui_MainWindow()
        # Gọi phương thức setupUi của đối tượng ui (được tạo từ lớp Ui_MainWindow) và truyền đối tượng hiện tại (self) vào làm đối số
        self.ui.setupUi(self)

        self.wait_upload_misson = 0
        self.ui.start.clicked.connect(lambda: asyncio.create_task(self.all()))
        """Window contain Video"""
        # create the video capture thread
        # self.thread_1 = VideoThread(0, video_1)

        # self.thread_2 = VideoThread(1, video_2)
        # self.thread_3 = VideoThread(2, video_3)
        # self.thread_4 = VideoThread(3, video_4)
        # self.thread_5 = VideoThread(4, video_5)
        # self.thread_6 = VideoThread(5, video_6)

        # start the thread
        # self.thread_1.start()

        # self.thread_2.start()
        # self.thread_3.start()
        # self.thread_4.start()
        # self.thread_5.start()
        # self.thread_6.start()

        # connect its signal to the update_image slot
        # self.thread_1.change_pixmap_signal.connect(self.update_1)

        # self.thread_2.change_pixmap_signal.connect(self.update_2)
        # self.thread_3.change_pixmap_signal.connect(self.update_3)
        # self.thread_4.change_pixmap_signal.connect(self.update_4)
        # self.thread_5.change_pixmap_signal.connect(self.update_5)
        # self.thread_6.change_pixmap_signal.connect(self.update_6)

        ##########################################################################################################################################################
        # Tạo biến toàn cục để kiểm tra xem có bao nhiêu con đã kết nối
        self.number_drone = 0
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))

        with open(
            f"{parent_dir}/data/ID_drone.txt", "r"
        ) as file:  # Đọc nội dung của file
            lines = file.readlines()  # Đọc tất cả các dòng trong file

        # Ghi đè nội dung của file với chuỗi trống
        with open(f"{parent_dir}/data/ID_drone.txt", "w") as file:
            file.write("")  # Xóa nội dung hiện tại của file

        """Điều khiển từng drone"""
        # Khối code connect từng drone
        # Khi nút connect_drone_1 được nhấn thì gọi đến hàm Connect_1() để kết nốt với uav thông qua các port
        self.ui.connect_drone_1.clicked.connect(
            lambda: asyncio.create_task(self.Connect_1())
        )
        self.ui.connect_drone_2.clicked.connect(
            lambda: asyncio.create_task(self.Connect_2())
        )
        self.ui.connect_drone_3.clicked.connect(
            lambda: asyncio.create_task(self.Connect_3())
        )
        self.ui.connect_drone_4.clicked.connect(
            lambda: asyncio.create_task(self.Connect_4())
        )
        self.ui.connect_drone_5.clicked.connect(
            lambda: asyncio.create_task(self.Connect_5())
        )
        self.ui.connect_drone_6.clicked.connect(
            lambda: asyncio.create_task(self.Connect_6())
        )

        # Khối code arm từng drone, đây là hàm kiểm tra an toàn trước khi bay
        # Khi nút arm_drone_1 được nhấn thì gọi đến hàm Arming_1() để thực hiện lệnh kiểm tra an toàn trước khi bay
        self.ui.arm_drone_1.clicked.connect(
            lambda: asyncio.create_task(self.Arming_1())
        )
        self.ui.arm_drone_2.clicked.connect(
            lambda: asyncio.create_task(self.Arming_2())
        )
        self.ui.arm_drone_3.clicked.connect(
            lambda: asyncio.create_task(self.Arming_3())
        )
        self.ui.arm_drone_4.clicked.connect(
            lambda: asyncio.create_task(self.Arming_4())
        )
        self.ui.arm_drone_5.clicked.connect(
            lambda: asyncio.create_task(self.Arming_5())
        )
        self.ui.arm_drone_6.clicked.connect(
            lambda: asyncio.create_task(self.Arming_6())
        )

        # Khối code disarm từng drone, đây là hàm kết thúc kiểm tra an toàn
        # Khi nút disarm_drone_1 được nhấn thì gọi đến hàm Disarm_1() để thực hiện lệnh kết thúc kiểm tra an toàn trước khi bay
        self.ui.disarm_drone_1.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_1())
        )
        self.ui.disarm_drone_2.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_2())
        )
        self.ui.disarm_drone_3.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_3())
        )
        self.ui.disarm_drone_4.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_4())
        )
        self.ui.disarm_drone_5.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_5())
        )
        self.ui.disarm_drone_6.clicked.connect(
            lambda: asyncio.create_task(self.Disarm_6())
        )

        # Khối code takeoff từng drone, đây là hàm cất cánh từng drone
        # Khi nút take_off_drone_1 được nhấn thì gọi đến hàm Take_off_1() để thực hiện lệnh cất cánh
        self.ui.take_off_drone_1.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_1())
        )
        self.ui.take_off_drone_2.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_2())
        )
        self.ui.take_off_drone_3.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_3())
        )
        self.ui.take_off_drone_4.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_4())
        )
        self.ui.take_off_drone_5.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_5())
        )
        self.ui.take_off_drone_6.clicked.connect(
            lambda: asyncio.create_task(self.Take_off_6())
        )

        # Khối code land từng drone, đây là hàm hạ cánh từng drone
        # Khi nút land_drone_1 được nhấn thì gọi đến hàm Land_1() để thực hiện lệnh hạ cánh
        self.ui.land_drone_1.clicked.connect(lambda: asyncio.create_task(self.Land_1()))
        self.ui.land_drone_2.clicked.connect(lambda: asyncio.create_task(self.Land_2()))
        self.ui.land_drone_3.clicked.connect(lambda: asyncio.create_task(self.Land_3()))
        self.ui.land_drone_4.clicked.connect(lambda: asyncio.create_task(self.Land_4()))
        self.ui.land_drone_5.clicked.connect(lambda: asyncio.create_task(self.Land_5()))
        self.ui.land_drone_6.clicked.connect(lambda: asyncio.create_task(self.Land_6()))

        # Khi nút land_drone_1 được nhấn thì gọi đến hàm Land_1() để thực hiện lệnh hạ cánh
        self.ui.return_and_land_drone_1.clicked.connect(
            lambda: asyncio.create_task(self.RTL_1())
        )
        self.ui.return_and_land_drone_2.clicked.connect(
            lambda: asyncio.create_task(self.RTL_2())
        )
        self.ui.return_and_land_drone_3.clicked.connect(
            lambda: asyncio.create_task(self.RTL_3())
        )
        self.ui.return_and_land_drone_4.clicked.connect(
            lambda: asyncio.create_task(self.RTL_4())
        )
        self.ui.return_and_land_drone_5.clicked.connect(
            lambda: asyncio.create_task(self.RTL_5())
        )
        self.ui.return_and_land_drone_6.clicked.connect(
            lambda: asyncio.create_task(self.RTL_6())
        )

        # Tạo biến toàn cục filename để liên kết giữa file nhiệm vụ được chọn và file để upload trong hàm nhiệm vụ
        self.filename_1 = None
        self.filename_2 = None
        self.filename_3 = None
        self.filename_4 = None
        self.filename_5 = None
        self.filename_6 = None

        # Khối code tải nhiệm vụ lên cho từng con một
        self.ui.Load_MS_1.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_1())
        )
        self.ui.Load_MS_2.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_2())
        )
        self.ui.Load_MS_3.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_3())
        )
        self.ui.Load_MS_4.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_4())
        )
        self.ui.Load_MS_5.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_5())
        )
        self.ui.Load_MS_6.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_6())
        )

        # Khối code mission từng drone, đây là hàm ra lệnh bắt đầu thực hiện nhiệm vụ cho từng drone
        # Khi nút mision_uav_1 được nhấn thì gọi đến hàm mision_drone_1() để thực hiện lệnh bắt đầu nhiệm vụ
        self.ui.mission_uav1.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_1())
        )
        self.ui.mission_uav2.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_2())
        )
        self.ui.mission_uav3.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_3())
        )
        self.ui.mission_uav4.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_4())
        )
        self.ui.mission_uav5.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_5())
        )
        self.ui.mission_uav6.clicked.connect(
            lambda: asyncio.create_task(self.mission_drone_6())
        )

        # Khối code ra lệnh cho từng con đến vị trí được chỉ định (kinh độ, vĩ độ)
        # Khi nút goto_1 được nhấn thì gọi đến hàm goto_1() để thực hiện lệnh cho uav đến vị trí được chỉ định
        self.ui.goto_1.clicked.connect(lambda: asyncio.create_task(self.goto_1()))
        self.ui.goto_2.clicked.connect(lambda: asyncio.create_task(self.goto_2()))
        self.ui.goto_3.clicked.connect(lambda: asyncio.create_task(self.goto_3()))
        self.ui.goto_4.clicked.connect(lambda: asyncio.create_task(self.goto_4()))
        self.ui.goto_5.clicked.connect(lambda: asyncio.create_task(self.goto_5()))
        self.ui.goto_6.clicked.connect(lambda: asyncio.create_task(self.goto_6()))

        # Khối code ra lệnh tạm dừng nhiệm vụ cho từng drone
        # Khi nút pause_1 được nhấn thì gọi đến hàm pause_1() để thực hiện lệnh UAV1 tạm dừng nhiệm vụ
        self.ui.pause_1.clicked.connect(lambda: asyncio.create_task(self.pause_1()))
        self.ui.pause_2.clicked.connect(lambda: asyncio.create_task(self.pause_2()))
        self.ui.pause_3.clicked.connect(lambda: asyncio.create_task(self.pause_3()))
        self.ui.pause_4.clicked.connect(lambda: asyncio.create_task(self.pause_4()))
        self.ui.pause_5.clicked.connect(lambda: asyncio.create_task(self.pause_5()))
        self.ui.pause_6.clicked.connect(lambda: asyncio.create_task(self.pause_6()))

        # Khi nút pushButton_3 được nhấn thì ta sẽ tiến hành gọi đến hàm photo_and_distance để khởi động quá trình detect bằng cách gọi đến code test3
        self.ui.pushButton_3.clicked.connect(
            lambda: asyncio.create_task(self.detect_object())
        )

        # Khi nút pushButton_4 được nhấn thì gọi đến hàm control_camera để mở code điều khiển camera trên drone
        self.ui.pushButton_4.clicked.connect(
            lambda: asyncio.create_task(self.control_camera())
        )

        # Khối code ra kệnh cho các uav gần nhất bay đến
        # Khi nhấn fly_1_uav thì gọi đến hàm button_1_uav để điều khiển một uav gần nhất đến tọa độ đối tượng
        self.ui.fly_1_uav.clicked.connect(
            lambda: asyncio.create_task(self.button_1_uav_clicked())
        )
        self.ui.fly_2_uav.clicked.connect(
            lambda: asyncio.create_task(self.button_2_uav_clicked())
        )
        self.ui.fly_3_UAV.clicked.connect(
            lambda: asyncio.create_task(self.button_3_uav_clicked())
        )
        self.ui.fly_4_UAV.clicked.connect(
            lambda: asyncio.create_task(self.button_4_uav_clicked())
        )

        # Map
        # Khi nút btn_map_all được nhấn thì gọi đến hàm open_map() để thực hiện mở map bản đồ
        self.ui.btn_map_all.clicked.connect(
            lambda: asyncio.create_task(self.open_map())
        )

        # Khối code lưu các tham số thay đổi
        # Khi nút save_1 được nhấn thì gọi đến hàm change_information_1 để thực hiện lệnh lưu các tham số thay đổi
        self.ui.save_1.clicked.connect(
            lambda: asyncio.create_task(self.change_information_1())
        )
        self.ui.save_2.clicked.connect(
            lambda: asyncio.create_task(self.change_information_2())
        )
        self.ui.save_3.clicked.connect(
            lambda: asyncio.create_task(self.change_information_3())
        )

        # Khởi tạo QTimer để cập nhật hình ảnh từ thư mục
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.timer4 = QTimer()
        self.timer5 = QTimer()
        # self.timer6 = QTimer(self)

        # Đặt thời gian quét thư mục
        # Sau 1s sẽ tiến hành quét thư viện hình ảnh trong file hung/xx1 một lần để cập nhật ảnh mới nhất lên giao diện
        self.timer1.start(1000)
        self.timer2.start(1000)
        self.timer3.start(1000)
        self.timer4.start(1000)
        self.timer5.start(1000)
        # self.timer6.start(1000)

        # Sau 1s nếu trong file hung/xx1->xx6 nếu có ảnh mới thì sẽ gọi đến hàm update để tiến hành cập nhật
        self.timer1.timeout.connect(self.update_image1)
        self.timer2.timeout.connect(self.update_image2)
        self.timer3.timeout.connect(self.update_image3)
        self.timer4.timeout.connect(self.update_image4)
        self.timer5.timeout.connect(self.update_image5)
        # self.timer6.timeout.connect(self.update_image6)

        # Thư mục chứa các tệp hình ảnh để sử dụng trong các hàm update_image1->6
        self.image_directory1 = f"{parent_dir}/logs/images/xx1"
        self.image_directory2 = f"{parent_dir}/logs/images/xx2"
        self.image_directory3 = f"{parent_dir}/logs/images/xx3"
        self.image_directory4 = f"{parent_dir}/logs/images/xx4"
        self.image_directory5 = f"{parent_dir}/logs/images/xx5"
        # self.image_directory6 = "./hung/xx6"

        # Tạo danh sách các tệp hình ảnh để sử dụng trong các hàm update_image1->6
        self.image_files1 = []
        self.image_files2 = []
        self.image_files3 = []
        self.image_files4 = []
        self.image_files5 = []
        # self.image_files6 = []

        ##################################################################################################################################################
        """Control 6 drone"""
        # connect multidrone
        self.ui.connect_all.clicked.connect(
            lambda: asyncio.create_task(self.connect_6_drone())
        )

        # takeoff multi drone
        self.ui.take_off_all.clicked.connect(
            lambda: asyncio.create_task(self.take_off_6_drone())
        )

        # arm multi drone
        self.ui.arm_all.clicked.connect(lambda: asyncio.create_task(self.arm_6_drone()))

        # land multi drone
        self.ui.land_all.clicked.connect(
            lambda: asyncio.create_task(self.land_6_drone())
        )

        # Return to land multi drone
        self.ui.RTL_all_2.clicked.connect(lambda: asyncio.create_task(self.RTL_ALL()))

        # Nạp nhiệm vụ cho các drone
        self.ui.Load_MS_all.clicked.connect(
            lambda: asyncio.create_task(self.upload_ms_all())
        )

        # Khởi động nhiệm vụ cho các drone
        self.ui.mission_all.clicked.connect(
            lambda: asyncio.create_task(self.mission_all())
        )
        self.ui.mission_all_2.clicked.connect(
            lambda: asyncio.create_task(self.mission_all())
        )

        # Khi nút goto_all được nhấn thì gọi đến hàm goto_all ra lệnh cho các drone đến vị trí tọa độ được chỉ định
        self.ui.goto_all.clicked.connect(lambda: asyncio.create_task(self.goto_all()))

        # Tạm dừng thực hiện nhiệm vụ các drone
        self.ui.pause_all.clicked.connect(lambda: asyncio.create_task(self.pause_all()))
        self.ui.pause_all_2.clicked.connect(
            lambda: asyncio.create_task(self.pause_all())
        )

        #################################################################################################################################################
        """Tạo chuyển động cho các trang"""
        # Xóa thanh tiêu đề cửa sổ
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Đặt nền chính thành trong suốt
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Hiệu ứng đổ bóng
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.ui.btn_home.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Áp dụng hiệu ứng đổ bóng vào widget trung tâm
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # Cài đặt biểu tượng cho cửa sổ
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/github.svg"))
        # Đặt tiêu đề cửa sổ
        self.setWindowTitle("MODERN UI")

        # Window Size grip to resize window
        QSizeGrip(self.ui.size_grip)

        # Thu nhỏ cửa sổ
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())

        # Đóng cửa sổ
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())

        # Mở rộng cửa sổ hoặc cho cửa sổ quay lại kích thước ban đầu
        self.ui.restore_window_button.clicked.connect(
            lambda: self.restore_or_maximize_window()
        )

        # Di chuyển cửa sổ khi kéo chuột trên thanh tiêu đề
        def moveWindow(e):
            # Kiểm tra kích thước cửa sổ có đang như mặc định hay không
            if self.isMaximized() == False:  # Không phải trang thái ban đầu
                # Chỉ di chuyển cửa sổ khi cửa sổ có kích thước bị thu nhỏ
                # Chỉ có thể di chuyển cửa sổ khi chuột trái được nhấp
                if e.buttons() == Qt.LeftButton:
                    # Di chuyển cửa sổ
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        # Sự kiện nhấp chuột/Sự kiện di chuyển chuột/sự kiện kéo vào tiêu đề trên cùng để di chuyển cửa sổ
        self.ui.header_frame.mouseMoveEvent = moveWindow

        # Nút chuyển đổi menu bên trái
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())
        self.show()

        # Các nút để truy cập từng trang
        # Khi nhấn btn_home thì gọi đến page_home được tạo bên file giao diện ui_interface
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        )
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.btn_home.setStyleSheet(
                "background-color: rgb(255, 255, 255);"
            )
        )  # Đổi màu nút
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.btn_connect.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.btn_map.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.btn_algorithm.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_home.clicked.connect(
            lambda: self.ui.btn_parameter.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )

        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_connect)
        )  # khi nhấn btn_connect thì gọi đến page_connect
        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.btn_connect.setStyleSheet(
                "background-color: rgb(255, 255, 255);"
            )
        )
        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.btn_home.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.btn_map.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.btn_algorithm.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_connect.clicked.connect(
            lambda: self.ui.btn_parameter.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )

        self.ui.btn_map.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_map)
        )  # Khi nhấn btn_map thì gọi đến page_map
        self.ui.btn_map.clicked.connect(
            lambda: self.ui.btn_map.setStyleSheet(
                "background-color: rgb(255, 255, 255);"
            )
        )
        self.ui.btn_map.clicked.connect(
            lambda: self.ui.btn_home.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_map.clicked.connect(
            lambda: self.ui.btn_connect.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_map.clicked.connect(
            lambda: self.ui.btn_algorithm.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_map.clicked.connect(
            lambda: self.ui.btn_parameter.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )

        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_algorithm))   # khi nhấn btn_algorithm thì gọi đến page_algorithm
        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(255, 255, 255);"))
        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(118, 118, 118);"))
        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(118, 118, 118);"))
        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(118, 118, 118);"))
        # self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(118, 118, 118);"))

        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_parameter)
        )  # Khi nhấn nút btn_parameter thì gọi đến page_parameter
        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.btn_parameter.setStyleSheet(
                "background-color: rgb(255, 255, 255);"
            )
        )
        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.btn_home.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.btn_connect.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.btn_map.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )
        self.ui.btn_parameter.clicked.connect(
            lambda: self.ui.btn_algorithm.setStyleSheet(
                "background-color: rgb(118, 118, 118);"
            )
        )

    # Menu trượt bên trái
    def slideLeftMenu(self):
        # Nhận chiều rộng menu bên trái hiện tại
        width = self.ui.slide_menu_container.width()

        # Nếu menu có chiều rộng bằng 0
        if width == 0:
            # Mở rộng menu
            newWidth = 200
            self.ui.open_close_side_bar_btn.setIcon(
                QtGui.QIcon(":/icons/icons/chevron-left.svg")
            )
        # Nếu menu có chiều rộng max
        else:
            # Trả về chiều rộng menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(
                QtGui.QIcon(":/icons/icons/align-justify.svg")
            )

        # Tạo chuyển động cho quá trình chuyển đổi
        self.animation = QPropertyAnimation(
            self.ui.slide_menu_container, b"maximumWidth"
        )  # Animate minimumWidht
        self.animation.setDuration(250)
        # Start value is the current menu width
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # Thêm sự kiện cho chuột vào cửa sổ
    def mousePressEvent(self, event):
        # Lấy vị trí hiện tại của chuột
        self.clickPosition = event.globalPos()
        # Chúng ta sẽ sử dụng giá trị này để di chuyển cửa sổ
    # Cập nhật biểu tượng nút phóng to hoặc thu nhỏ trên cửa sổ

    def restore_or_maximize_window(self):
        # Nếu cửa sổ mở max
        if self.isMaximized():
            self.showNormal()
            # Thay đổi icon
            self.ui.restore_window_button.setIcon(
                QtGui.QIcon(":/icons/icons/maximize-2.svg")
            )
        else:
            self.showMaximized()
            # Thay đổi icon
            self.ui.restore_window_button.setIcon(
                QtGui.QIcon(":/icons/icons/minimize-2.svg")
            )

    # 3333
    # Hàm mở code Map

    async def open_map(self):
        command = f"python3 {parent_dir}/map/DG5.py"
        os.system(f"gnome-terminal -- /bin/bash -c '{command}; exec /bin/bash' &")

    ##################################################################################################################################
    """Các hàm update ảnh cho từng drone"""
    # update image1

    def update_image1(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files1 = sorted(self.get_image_files1(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files1 != self.image_files1:
            self.image_files1 = new_image_files1
            if self.image_files1:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file1 = self.image_files1[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path1 = os.path.join(self.image_directory1, first_file1)
                pixmap1 = QPixmap(file_path1)
                # Gán hình ảnh vào widget label_35
                self.ui.label_35.setPixmap(pixmap1)
                # Thay đổi kích cõ hình ảnh theo khung hình label 35
                self.ui.label_35.setScaledContents(True)
            else:
                print("No image files found in the directory")

    # Tạo danh sách tập hợp các ảnh có đuôi jpg chứa trong đường dẫn image_directory1
    def get_image_files1(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory1) if f.endswith(".jpg")]

    # update image2
    def update_image2(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files2 = sorted(self.get_image_files2(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files2 != self.image_files2:
            self.image_files2 = new_image_files2
            if self.image_files2:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file2 = self.image_files2[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path2 = os.path.join(self.image_directory2, first_file2)
                pixmap2 = QPixmap(file_path2)
                self.ui.label_36.setPixmap(pixmap2)
                self.ui.label_36.setScaledContents(True)
            else:
                print("No image files found in the directory")

    def get_image_files2(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory2) if f.endswith(".jpg")]

    # update image3
    def update_image3(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files3 = sorted(self.get_image_files3(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files3 != self.image_files3:
            self.image_files3 = new_image_files3
            if self.image_files3:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file3 = self.image_files3[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path3 = os.path.join(self.image_directory3, first_file3)
                pixmap3 = QPixmap(file_path3)
                self.ui.label_37.setPixmap(pixmap3)
                self.ui.label_37.setScaledContents(True)
            else:
                print("No image files found in the directory")

    def get_image_files3(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory3) if f.endswith(".jpg")]

    # update image4
    def update_image4(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files4 = sorted(self.get_image_files4(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files4 != self.image_files4:
            self.image_files4 = new_image_files4
            if self.image_files4:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file4 = self.image_files4[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path4 = os.path.join(self.image_directory4, first_file4)
                pixmap4 = QPixmap(file_path4)
                self.ui.label_38.setPixmap(pixmap4)
                self.ui.label_38.setScaledContents(True)
            else:
                print("No image files found in the directory")

    def get_image_files4(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory4) if f.endswith(".jpg")]

    # update image5
    def update_image5(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files5 = sorted(self.get_image_files5(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files5 != self.image_files5:
            self.image_files5 = new_image_files5
            if self.image_files5:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file5 = self.image_files5[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path5 = os.path.join(self.image_directory5, first_file5)
                pixmap5 = QPixmap(file_path5)
                self.ui.label_39.setPixmap(pixmap5)
                self.ui.label_39.setScaledContents(True)
            else:
                print("No image files found in the directory")

    def get_image_files5(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory5) if f.endswith(".jpg")]

    # update image6
    """
    def update_image6(self):
        # Lấy danh sách các tệp hình ảnh trong thư mục và sắp xếp theo thứ tự bảng chữ cái
        new_image_files6 = sorted(self.get_image_files6(), reverse=True)
        # Kiểm tra xem có sự thay đổi trong danh sách các tệp hình ảnh không
        if new_image_files6 != self.image_files6:
            self.image_files6 = new_image_files6
            if self.image_files6:
                # Lấy tệp hình ảnh đầu tiên trong danh sách đã sắp xếp
                first_file6 = self.image_files6[0]
                # Đường dẫn đầy đủ của tệp hình ảnh
                file_path6 = os.path.join(self.image_directory6, first_file6)
                pixmap6 = QPixmap(file_path6)
                self.ui.label_40.setPixmap(pixmap6)
                self.ui.label_40.setScaledContents(True)
            else:
                print("No image files found in the directory")

    def get_image_files6(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory6) if f.endswith(".jpg")]
    """
    #########################################################################################################################################
    """Các hàm connect từng drone"""
    # Connect drone 1

    async def Connect_1(self):
        global drone_1
        print("--Connecting to Drone 1")
        self.ui.drone_status_1.appendPlainText(
            "--Connecting to Drone 1"
        )  # In ra cửa sổ drone_status
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 1")
        await drone_1.connect()  # drone1 tiến hành connect
        print("--Drone 1 Connected")
        await drone_1.action.set_maximum_speed(1.0)
        self.ui.drone_status_1.appendPlainText("--Drone 1 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 1 Connected")
        # set widget label có tên waiting_connect_1 hiển thị nội dung "Drone1 connected"
        self.ui.waiting_connect_1.setText("Drone1 connected")
        self.ui.waiting_connect_1.setStyleSheet(
            "color: rgb(0,255,0);"
        )  # đổi màu chữ của label
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}./data/ID_drone.txt", "a") as f:
            f.write(str(1) + "\n")
        await asyncio.gather(
            self.get_alt_1(),
            self.get_arm_1(),
            self.get_batt_1(),
            self.get_mode_1(),
            self.get_gps_1(),
            # Sau khi kết nối thành công thì gọi đến các hàm lấy thông tin
            self.print_status_text_1(),
            self.information_1(),
        )
        return None

    # Connect drone 2
    async def Connect_2(self):
        global drone_2
        print("--Connecting to Drone 2")
        self.ui.drone_status_2.appendPlainText("--Connecting to Drone 2")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 2")
        await drone_2.connect()
        print("--Drone 2 Connected")
        await drone_2.action.set_maximum_speed(1.0)
        self.ui.drone_status_2.appendPlainText("--Drone 2 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 2 Connected")
        self.ui.waiting_connect_2.setText("Drone2 connected")
        self.ui.waiting_connect_2.setStyleSheet("color: rgb(0,255,0);")
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}/data/ID_drone.txt", "a") as f:
            f.write(str(2) + "\n")
        await asyncio.gather(
            self.get_alt_2(),
            self.get_arm_2(),
            self.get_batt_2(),
            self.get_mode_2(),
            self.get_gps_2(),
            self.print_status_text_2(),
            self.information_2(),
        )
        return None

    # Connect drone 3
    async def Connect_3(self):
        global drone_3
        print("--Connecting to Drone 3")
        self.ui.drone_status_3.appendPlainText("--Connecting to Drone 3")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 3")
        await drone_3.connect()
        print("--Drone 3 Connected")
        await drone_3.action.set_maximum_speed(1.0)
        self.ui.drone_status_3.appendPlainText("--Drone 3 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 3 Connected")
        self.ui.waiting_connect_3.setText("Drone3 connected")
        self.ui.waiting_connect_3.setStyleSheet("color: rgb(0,255,0);")
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}/data/ID_drone.txt", "a") as f:
            f.write(str(3) + "\n")
        await asyncio.gather(
            self.get_alt_3(),
            self.get_arm_3(),
            self.get_batt_3(),
            self.get_mode_3(),
            self.get_gps_3(),
            self.print_status_text_3(),
        )
        return None

    # Connect drone 4
    async def Connect_4(self):
        global drone_4
        print("--Connecting to Drone 4")
        self.ui.drone_status_4.appendPlainText("--Connecting to Drone 4")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 4")
        await drone_4.connect()
        print("--Drone 4 Connected")
        await drone_4.action.set_maximum_speed(1.0)
        self.ui.drone_status_4.appendPlainText("--Drone 4 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 4 Connected")
        self.ui.waiting_connect_4.setText("Drone4 connected")
        self.ui.waiting_connect_4.setStyleSheet("color: rgb(0,255,0);")
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}/data/ID_drone.txt", "a") as f:
            f.write(str(4) + "\n")
        await asyncio.gather(
            self.get_alt_4(),
            self.get_arm_4(),
            self.get_batt_4(),
            self.get_mode_4(),
            self.get_gps_4(),
            self.print_status_text_4(),
        )
        return None

    # Connect drone 5
    async def Connect_5(self):
        global drone_5
        print("--Connecting to Drone 5")
        self.ui.drone_status_5.appendPlainText("--Connecting to Drone 5")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 5")
        await drone_5.connect()
        print("--Drone 5 Connected")
        await drone_5.action.set_maximum_speed(1.0)
        self.ui.drone_status_5.appendPlainText("--Drone 5 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 5 Connected")
        self.ui.waiting_connect_5.setText("Drone5 connected")
        self.ui.waiting_connect_5.setStyleSheet("color: rgb(0,255,0);")
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}/data/ID_drone.txt", "a") as f:
            f.write(str(5) + "\n")
        await asyncio.gather(
            self.get_alt_5(),
            self.get_arm_5(),
            self.get_batt_5(),
            self.get_mode_5(),
            self.get_gps_5(),
            self.print_status_text_5(),
        )
        return None

    # Connect drone 6
    async def Connect_6(self):
        global drone_6
        print("--Connecting to Drone 6")
        self.ui.drone_status_6.appendPlainText("--Connecting to Drone 6")
        await drone_6.connect()
        print("--Drone 6 Connected")
        await drone_6.action.set_maximum_speed(1.0)
        self.ui.drone_status_6.appendPlainText("--Drone 6 Connected")
        self.ui.waiting_connect_6.setText("Drone6 connected")
        self.ui.waiting_connect_6.setStyleSheet("color: rgb(0,255,0);")
        self.number_drone = self.number_drone + 1
        with open(f"{parent_dir}/data/drone_num.txt", "w") as f:
            f.write(str(self.number_drone))
        with open(f"{parent_dir}/data/ID_drone.txt", "a") as f:
            f.write(str(6) + "\n")
        await asyncio.gather(
            self.get_alt_6(),
            self.get_arm_6(),
            self.get_batt_6(),
            self.get_mode_6(),
            self.get_gps_6(),
            self.print_status_text_6(),
        )
        return None

    #########################################################################################################################################
    """Các hàm arm từng drone"""
    # arm drone 1

    async def Arming_1(self):
        print("Arming Drone 1...")
        self.ui.drone_status_1.appendPlainText("Arming Drone 1...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 1...")
        await drone_1.action.arm()
        print("Drone 1 Armed.")
        self.ui.drone_status_1.appendPlainText("Drone 1 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 1 Armed")
        self.ui.arm_or_disarm_drone1.setText("Drone 1 Armed")
        self.ui.arm_or_disarm_drone1.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_1.action.disarm()
        print("Drone 1 Disarmed.")
        self.ui.drone_status_1.appendPlainText("Drone 1 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 1 Disarm")
        self.ui.arm_or_disarm_drone1.setText("Drone 1 Disarm")
        self.ui.arm_or_disarm_drone1.setStyleSheet("color: rgb(0,255,0);")
        return None

    # arm drone 2
    async def Arming_2(self):
        print("Arming Drone 2...")
        self.ui.drone_status_2.appendPlainText("Arming Drone 2...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 2...")
        await drone_2.action.arm()
        print("Drone 2 Armed.")
        self.ui.drone_status_2.appendPlainText("Drone 2 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 2 Armed")
        self.ui.arm_or_disarm_drone2.setText("Drone 2 Armed")
        self.ui.arm_or_disarm_drone2.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_2.action.disarm()
        print("Drone 2 Disarmed.")
        self.ui.drone_status_2.appendPlainText("Drone 2 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 2 Disarm")
        self.ui.arm_or_disarm_drone2.setText("Drone 2 Disarm")
        self.ui.arm_or_disarm_drone2.setStyleSheet("color: rgb(0,255,0);")
        return None

    # arm drone 3
    async def Arming_3(self):
        print("Arming Drone 3...")
        self.ui.drone_status_3.appendPlainText("Arming Drone 3...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 3...")
        await drone_3.action.arm()
        print("Drone 3 Armed.")
        self.ui.drone_status_3.appendPlainText("Drone 3 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 3 Armed")
        self.ui.arm_or_disarm_drone3.setText("Drone 3 Armed")
        self.ui.arm_or_disarm_drone3.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_3.action.disarm()
        print("Drone 3 Disarmed.")
        self.ui.drone_status_3.appendPlainText("Drone 3 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 3 Disarm")
        self.ui.arm_or_disarm_drone3.setText("Drone 3 Disarm")
        self.ui.arm_or_disarm_drone3.setStyleSheet("color: rgb(0,255,0);")
        return None

    # arm drone 4
    async def Arming_4(self):
        print("Arming Drone 4...")
        self.ui.drone_status_4.appendPlainText("Arming Drone 4...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 4...")
        await drone_4.action.arm()
        print("Drone 4 Armed.")
        self.ui.drone_status_4.appendPlainText("Drone 4 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 4 Armed")
        self.ui.arm_or_disarm_drone4.setText("Drone 4 Armed")
        self.ui.arm_or_disarm_drone4.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_4.action.disarm()
        print("Drone 4 Disarmed.")
        self.ui.drone_status_4.appendPlainText("Drone 4 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 4 Disarm")
        self.ui.arm_or_disarm_drone4.setText("Drone 4 Disarm")
        self.ui.arm_or_disarm_drone4.setStyleSheet("color: rgb(0,255,0);")
        return None

    # arm drone 5
    async def Arming_5(self):
        print("Arming Drone 5...")
        self.ui.drone_status_5.appendPlainText("Arming Drone 5...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 5...")
        await drone_5.action.arm()
        print("Drone 5 Armed.")
        self.ui.drone_status_5.appendPlainText("Drone 5 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 5 Armed")
        self.ui.arm_or_disarm_drone5.setText("Drone 5 Armed")
        self.ui.arm_or_disarm_drone5.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_5.action.disarm()
        print("Drone 5 Disarmed.")
        self.ui.drone_status_5.appendPlainText("Drone 5 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 5 Disarm")
        self.ui.arm_or_disarm_drone5.setText("Drone 5 Disarm")
        self.ui.arm_or_disarm_drone5.setStyleSheet("color: rgb(0,255,0);")
        return None

    # arm drone 6
    async def Arming_6(self):
        print("Arming Drone 6...")
        self.ui.drone_status_6.appendPlainText("Arming Drone 6...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Arming Drone 6...")
        await drone_6.action.arm()
        print("Drone 6 Armed.")
        self.ui.drone_status_6.appendPlainText("Drone 6 Armed")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 6 Armed")
        self.ui.arm_or_disarm_drone6.setText("Drone 6 Armed")
        self.ui.arm_or_disarm_drone6.setStyleSheet("color: rgb(0,255,0);")
        await asyncio.sleep(5)
        await drone_6.action.disarm()
        print("Drone 6 Disarmed.")
        self.ui.drone_status_6.appendPlainText("Drone 6 Disarm")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("Drone 6 Disarm")
        self.ui.arm_or_disarm_drone6.setText("Drone 6 Disarm")
        self.ui.arm_or_disarm_drone6.setStyleSheet("color: rgb(0,255,0);")
        return None

    #######################################################################################################################################
    """Các hàm disarm từng drone"""
    # disarm drone 1

    async def Disarm_1(self):
        print("DisArming...")
        await drone_1.action.disarm()
        print("Drone 1 Disarmed.")
        self.ui.arm_or_disarm_drone1.setText("Drone 1 Disarmed")
        self.ui.arm_or_disarm_drone1.setStyleSheet("color: rgb(0,255,0);")
        return None

    # disarm drone 2
    async def Disarm_2(self):
        print("DisArming...")
        await drone_2.action.disarm()
        print("Drone 2 Disarmed.")
        self.ui.arm_or_disarm_drone2.setText("Drone 2 Disarmed")
        self.ui.arm_or_disarm_drone2.setStyleSheet("color: rgb(0,255,0);")
        return None

    # disarm drone 3
    async def Disarm_3(self):
        print("DisArming...")
        await drone_3.action.disarm()
        print("Drone 3 Disarmed.")
        self.ui.arm_or_disarm_drone3.setText("Drone 3 Disarmed")
        self.ui.arm_or_disarm_drone3.setStyleSheet("color: rgb(0,255,0);")
        return None

    # disarm drone 4
    async def Disarm_4(self):
        print("DisArming...")
        await drone_4.action.disarm()
        print("Drone 4 Disarmed.")
        self.ui.arm_or_disarm_drone4.setText("Drone 4 Disarmed")
        self.ui.arm_or_disarm_drone4.setStyleSheet("color: rgb(0,255,0);")
        return None

    # disarm drone 5
    async def Disarm_5(self):
        print("DisArming...")
        await drone_5.action.disarm()
        print("Drone 5 Disarmed.")
        self.ui.arm_or_disarm_drone5.setText("Drone 5 Disarmed")
        self.ui.arm_or_disarm_drone5.setStyleSheet("color: rgb(0,255,0);")
        return None

    # disarm drone 6
    async def Disarm_6(self):
        print("DisArming...")
        await drone_6.action.disarm()
        print("Drone 6 Disarmed.")
        self.ui.arm_or_disarm_drone6.setText("Drone 6 Disarmed")
        self.ui.arm_or_disarm_drone6.setStyleSheet("color: rgb(0,255,0);")
        return None

    #######################################################################################################################################
    """Các hàm takeoff từng drone"""
    # takeoff drone 1

    async def Take_off_1(self):
        # gán giá trị độ cao được nhập vào cho biến high_take_off_1
        high_take_off_1 = float(self.ui.edit_high_drone_1.toPlainText())
        if (
            high_take_off_1 > 0
        ):  # Nếu giá trị được gán >0 thì thực hiện các lệnh bên trong
            print("-- Initializing drone 1")
            self.ui.drone_status_1.appendPlainText("-- Initializing drone 1")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 1")
            print("-- Arming drone 1")
            self.ui.drone_status_1.appendPlainText("-- Arming drone 1")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 1")
            await drone_1.action.arm()
            print("--Taking off drone 1...")
            self.ui.drone_status_1.appendPlainText("--Taking off drone 1...")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Taking off drone 1...")
            # set độ cao để takeoff
            await drone_1.action.set_takeoff_altitude(high_take_off_1)
            await drone_1.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_1.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    # takeoff drone 2
    async def Take_off_2(self):
        high_take_off_2 = float(self.ui.edit_high_drone_2.toPlainText())
        if high_take_off_2 > 0:
            print("-- Initializing drone 2")
            self.ui.drone_status_2.appendPlainText("-- Initializing drone 2")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 2")
            print("-- Arming drone 2")
            await drone_2.action.arm()
            print("--Taking off drone 2...")
            self.ui.drone_status_2.appendPlainText("-- Arming drone 2")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 2")
            await drone_2.action.set_takeoff_altitude(high_take_off_2)
            await drone_2.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_2.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    # takeoff drone 3
    async def Take_off_3(self):
        high_take_off_3 = float(self.ui.edit_high_drone_3.toPlainText())
        if high_take_off_3 > 0:
            print("-- Initializing drone 3")
            self.ui.drone_status_3.appendPlainText("-- Initializing drone 3")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 3")
            print("-- Arming drone 3")
            await drone_3.action.arm()
            print("--Taking off drone 3...")
            self.ui.drone_status_3.appendPlainText("-- Arming drone 3")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 3")
            await drone_3.action.set_takeoff_altitude(high_take_off_3)
            await drone_3.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_3.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    # takeoff drone 4
    async def Take_off_4(self):
        high_take_off_4 = float(self.ui.edit_high_drone_4.toPlainText())
        if high_take_off_4 > 0:
            print("-- Initializing drone 4")
            self.ui.drone_status_4.appendPlainText("-- Initializing drone 4")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 4")
            print("-- Arming drone 4")
            await drone_4.action.arm()
            print("--Taking off drone 4...")
            self.ui.drone_status_4.appendPlainText("-- Arming drone 4")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 4")
            await drone_4.action.set_takeoff_altitude(high_take_off_4)
            await drone_4.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_4.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    # takeoff drone 5
    async def Take_off_5(self):
        high_take_off_5 = float(self.ui.edit_high_drone_5.toPlainText())
        if high_take_off_5 > 0:
            print("-- Initializing drone 5")
            self.ui.drone_status_5.appendPlainText("-- Initializing drone 5")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 5")
            print("-- Arming drone 5")
            await drone_5.action.arm()
            print("--Taking off drone 5...")
            self.ui.drone_status_5.appendPlainText("-- Arming drone 5")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 5")
            await drone_5.action.set_takeoff_altitude(high_take_off_5)
            await drone_5.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_5.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    # takeoff drone 6
    async def Take_off_6(self):
        high_take_off_6 = float(self.ui.edit_high_drone_6.toPlainText())
        if high_take_off_6 > 0:
            print("-- Initializing drone 6")
            self.ui.drone_status_6.appendPlainText("-- Initializing drone 6")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Initializing drone 6")
            print("-- Arming drone 6")
            await drone_6.action.arm()
            print("--Taking off drone 6...")
            self.ui.drone_status_6.appendPlainText("-- Arming drone 6")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Arming drone 6")
            await drone_6.action.set_takeoff_altitude(high_take_off_6)
            await drone_6.action.takeoff()
        else:
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_6.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )
            self.ui.plainTextEdit_all_6_uav.appendPlainText(
                "Please enter a valid altitude for takeoff! (valid >0 )"
            )

    #######################################################################################################################################
    """Các hàm land từng drone"""
    # land drone 1

    async def Land_1(self):
        await drone_1.action.land()  # Hạ cánh drone_1
        print("--Landing drone 1...")
        self.ui.drone_status_1.appendPlainText("--Landing drone 1...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 1...")

    # land drone 2
    async def Land_2(self):
        await drone_2.action.land()
        print("--Landing drone 2...")
        self.ui.drone_status_2.appendPlainText("--Landing drone 2...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 2...")

    # land drone 3
    async def Land_3(self):
        await drone_3.action.land()
        print("--Landing drone 3...")
        self.ui.drone_status_3.appendPlainText("--Landing drone 3...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 3...")

    # land drone 4
    async def Land_4(self):
        await drone_4.action.land()
        print("--Landing drone 4...")
        self.ui.drone_status_4.appendPlainText("--Landing drone 4...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 4...")

    # land drone 5
    async def Land_5(self):
        await drone_5.action.land()
        print("--Landing drone 5...")
        self.ui.drone_status_5.appendPlainText("--Landing drone 5...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 5...")

    # land drone 6
    async def Land_6(self):
        await drone_6.action.land()
        print("--Landing drone 6...")
        self.ui.drone_status_6.appendPlainText("--Landing drone 6...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 6...")

    #######################################################################################################################################
    """Các hàm mission từng drone"""
    # mission drone 1

    async def mission_drone_1(self):
        await drone_1.action.arm()
        print("--Mission drone 1")
        self.ui.file_uav1.appendPlainText("--Mission drone 1")
        self.ui.file_all_uav.appendPlainText("--Mission drone 1")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 1")
        await drone_1.mission.start_mission()  # Bắt đầu thực hiện nhiệm vụ
        async for mission_progress in drone_1.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_1()
                break

    # mission drone 2
    async def mission_drone_2(self):
        await drone_2.action.arm()
        print("--Mission drone 2")
        self.ui.file_uav2.appendPlainText("--Mission drone 2")
        self.ui.file_all_uav.appendPlainText("--Mission drone 2")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 2")
        await drone_2.mission.start_mission()
        async for mission_progress in drone_2.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_2()
                break

    # mission drone 3
    async def mission_drone_3(self):
        await drone_3.action.arm()
        print("--Mission drone 3")
        self.ui.file_uav3.appendPlainText("--Mission drone 3")
        self.ui.file_all_uav.appendPlainText("--Mission drone 3")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 3")
        await drone_3.mission.start_mission()
        async for mission_progress in drone_3.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_3()
                break

    # mission drone 4
    async def mission_drone_4(self):
        await drone_4.action.arm()
        print("--Mission drone 4")
        self.ui.file_uav4.appendPlainText("--Mission drone 4")
        self.ui.file_all_uav.appendPlainText("--Mission drone 4")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 4")
        await drone_4.mission.start_mission()
        async for mission_progress in drone_4.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_4()
                break

    # mission drone 5
    async def mission_drone_5(self):
        await drone_5.action.arm()
        print("--Mission drone 5")
        self.ui.file_uav5.appendPlainText("--Mission drone 5")
        self.ui.file_all_uav.appendPlainText("--Mission drone 5")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 5")
        await drone_5.mission.start_mission()
        async for mission_progress in drone_5.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_5()
                break

    # mission drone 6
    async def mission_drone_6(self):
        await drone_6.action.arm()
        print("--Mission drone 6")
        self.ui.file_uav6.appendPlainText("--Mission drone 6")
        self.ui.file_all_uav.appendPlainText("--Mission drone 6")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 6")
        high_take_off_6 = float(self.ui.edit_high_drone_6.toPlainText())
        await self.Take_off_6()
        await drone_6.mission.start_mission()
        async for mission_progress in drone_6.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await asyncio.sleep(10)
                await self.RTL_6()
                await self.RTL_2()
                await self.RTL_1()
                break

    ########################################################################################################################################
    """Các hàm upload nhiệm vụ cho từng drone"""
    # Upload mission drone 1

    async def upload_ms_1(self):
        with open(f"{parent_dir}/logs/points/points1.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav1.setPlainText(file_content)

        mission_items_1 = []
        # Gán độ cao cho biến hight1 được đọc từ edit_high_drone_1
        hight1 = float(self.ui.edit_high_drone_1.toPlainText())
        # Tiến hàn đọc giá trị tọa độ từ file points1.txt để nạp vào nhiệm vụ
        with open(f"{parent_dir}/logs/points/points1.txt", "r") as file:
            for line in file:
                lat1, lon1 = map(float, line.strip().split(", "))
                mission_item_1 = MissionItem(
                    lat1,
                    lon1,
                    hight1,
                    float("nan"),
                    False,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    10,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_1.append(mission_item_1)
        mission_plan_1 = MissionPlan(mission_items_1)
        await asyncio.sleep(1)
        # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu
        await drone_1.mission.set_return_to_launch_after_mission(True)
        # Lệnh upload nhiệm vụ
        await drone_1.mission.upload_mission(mission_plan_1)
        print("-- Drone 1 upload mission: Done")
        self.ui.file_uav1.appendPlainText("-- Drone 1 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 1 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 1 upload mission: Done"
        )
        self.wait_upload_misson = self.wait_upload_misson + 1

    # Upload mission drone 2
    async def upload_ms_2(self):
        with open(f"{parent_dir}/logs/points/points2.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav2.setPlainText(file_content)

        mission_items_2 = []
        hight2 = float(self.ui.edit_high_drone_2.toPlainText())
        with open(f"{parent_dir}/logs/points/points2.txt", "r") as file:
            for line in file:
                lat2, lon2 = map(float, line.strip().split(", "))
                mission_item_2 = MissionItem(
                    lat2,
                    lon2,
                    hight2,
                    float("nan"),
                    False,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    10,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_2.append(mission_item_2)
        mission_plan_2 = MissionPlan(mission_items_2)
        await asyncio.sleep(1)
        await drone_2.mission.set_return_to_launch_after_mission(True)
        await drone_2.mission.upload_mission(mission_plan_2)
        print("-- Drone 2 upload mission: Done")
        self.ui.file_uav2.appendPlainText("-- Drone 2 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 2 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 2 upload mission: Done"
        )
        self.wait_upload_misson = self.wait_upload_misson + 1

    # Upload mission drone 3
    async def upload_ms_3(self):
        with open(f"{parent_dir}/logs/points/points3.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav3.setPlainText(file_content)

        mission_items_3 = []
        hight3 = float(self.ui.edit_high_drone_3.toPlainText())
        with open(f"{parent_dir}/logs/points/points3.txt" "r") as file:
            for line in file:
                lat3, lon3 = map(float, line.strip().split(", "))
                mission_item_3 = MissionItem(
                    lat3,
                    lon3,
                    hight3,
                    float("nan"),
                    False,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    10,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_3.append(mission_item_3)
        mission_plan_3 = MissionPlan(mission_items_3)
        await asyncio.sleep(2)
        await drone_3.mission.upload_mission(mission_plan_3)
        print("-- Drone 3 upload mission: Done")
        self.ui.file_uav3.appendPlainText("-- Drone 3 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 3 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 3 upload mission: Done"
        )
        self.wait_upload_misson = self.wait_upload_misson + 1

    # Upload mission drone 4
    async def upload_ms_4(self):
        with open(f"{parent_dir}/logs/points/points4.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav4.setPlainText(file_content)

        mission_items_4 = []
        hight4 = float(self.ui.edit_high_drone_4.toPlainText())
        with open(f"{parent_dir}/logs/points/points4.txt", "r") as file:
            for line in file:
                lat4, lon4 = map(float, line.strip().split(", "))
                mission_item_4 = MissionItem(
                    lat4,
                    lon4,
                    hight4,
                    float("nan"),
                    False,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    10,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_4.append(mission_item_4)
        mission_plan_4 = MissionPlan(mission_items_4)
        await asyncio.sleep(3)
        await drone_4.mission.upload_mission(mission_plan_4)
        print("-- Drone 4 upload mission: Done")
        self.ui.file_uav4.appendPlainText("-- Drone 4 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 4 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 4 upload mission: Done"
        )
        self.wait_upload_misson = self.wait_upload_misson + 1

    # Upload mission drone 5
    async def upload_ms_5(self):
        with open(f"{parent_dir}/logs/points/points5.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav5.setPlainText(file_content)

        mission_items_5 = []
        hight5 = float(self.ui.edit_high_drone_5.toPlainText())
        with open(f"{parent_dir}/logs/points/points5.txt", "r") as file:
            for line in file:
                lat5, lon5 = map(float, line.strip().split(", "))
                mission_item_5 = MissionItem(
                    lat5,
                    lon5,
                    hight5,
                    float("nan"),
                    False,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    10,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_5.append(mission_item_5)
        mission_plan_5 = MissionPlan(mission_items_5)
        await asyncio.sleep(4)
        await drone_5.mission.upload_mission(mission_plan_5)
        self.ui.file_uav5.appendPlainText("-- Drone 5 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 5 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 5 upload mission: Done"
        )
        self.wait_upload_misson = self.wait_upload_misson + 1

    # Upload mission drone 6
    async def upload_ms_6(self):
        with open(f"{parent_dir}/logs/detect/detect.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav6.setPlainText(file_content)

        mission_items_6 = []
        hight6 = float(self.ui.edit_high_drone_6.toPlainText())
        folder_path = "detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            for line in file:
                lat6, lon6 = map(float, line.strip().split(", "))
                mission_item_6 = MissionItem(
                    lat6,
                    lon6,
                    hight6,
                    float("nan"),
                    True,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
                mission_items_6.append(mission_item_6)
        mission_plan_6 = MissionPlan(mission_items_6)
        await asyncio.sleep(5)
        await drone_6.mission.upload_mission(mission_plan_6)
        self.ui.file_uav6.appendPlainText("-- Drone 6 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 6 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "-- Drone 6 upload mission: Done"
        )
        await self.mission_drone_6()

    #######################################################################################################################################
    # Go to drone 1
    async def goto_1(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_1.telemetry.position():
            height = position.absolute_altitude_m
            await drone_1.action.goto_location(latitude, longtitude, height, 0)

    # Go to drone 2

    async def goto_2(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_2.telemetry.position():
            hight2 = position.absolute_altitude_m
            await drone_2.action.goto_location(latitude, longtitude, hight2, 0)

    # Go to drone 3
    async def goto_3(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_3.telemetry.position():
            hight3 = position.absolute_altitude_m
            await drone_3.action.goto_location(latitude, longtitude, hight3, 0)

    # Go to drone 4
    async def goto_4(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_4.telemetry.position():
            hight4 = position.absolute_altitude_m
            await drone_4.action.goto_location(latitude, longtitude, hight4, 0)

    # Go to drone 5
    async def goto_5(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_5.telemetry.position():
            hight5 = position.absolute_altitude_m
            await drone_5.action.goto_location(latitude, longtitude, hight5, 0)

    # Go to drone 6
    async def goto_6(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_6.telemetry.position():
            hight6 = position.absolute_altitude_m
            await drone_6.action.goto_location(latitude, longtitude, hight6, 0)

    #######################################################################################################################################
    # RTL drone 1
    async def RTL_1(self):
        L1 = float(self.ui.edit_high_drone_1.toPlainText())
        await drone_1.action.set_return_to_launch_altitude(L1)
        await drone_1.action.return_to_launch()

    # RTL drone 2
    async def RTL_2(self):
        L2 = float(self.ui.edit_high_drone_2.toPlainText())
        await drone_2.action.set_return_to_launch_altitude(L2)
        await drone_2.action.return_to_launch()

    # RTL drone 3
    async def RTL_3(self):
        L3 = float(self.ui.edit_high_drone_3.toPlainText())
        await asyncio.sleep(1)
        await drone_3.action.set_return_to_launch_altitude(L3)
        await drone_3.action.return_to_launch()

    # RTL drone 4
    async def RTL_4(self):
        L4 = float(self.ui.edit_high_drone_4.toPlainText())
        await drone_4.action.set_return_to_launch_altitude(L4)
        await drone_4.action.return_to_launch()

    # RTL drone 5
    async def RTL_5(self):
        L5 = float(self.ui.edit_high_drone_5.toPlainText())
        await drone_5.action.set_return_to_launch_altitude(L5)
        await drone_5.action.return_to_launch()

    # RTL drone 6
    async def RTL_6(self):
        L6 = float(self.ui.edit_high_drone_6.toPlainText())
        await drone_6.action.set_return_to_launch_altitude(L6)
        await drone_6.action.return_to_launch()

    #######################################################################################################################################
    # Pause mission drone 1
    async def pause_1(self):
        await drone_1.mission.pause_mission()

    # Pause mission drone 2
    async def pause_2(self):
        await drone_2.mission.pause_mission()

    # Pause mission drone 3
    async def pause_3(self):
        await drone_3.mission.pause_mission()

    # Pause mission drone 4
    async def pause_4(self):
        await drone_4.mission.pause_mission()

    # Pause mission drone 5
    async def pause_5(self):
        await drone_5.mission.pause_mission()

    # Pause mission drone 6
    async def pause_6(self):
        await drone_6.mission.pause_mission()

    #######################################################################################################################################
    # connect 6 drone
    async def connect_6_drone(self):
        await asyncio.gather(
            self.Connect_1(),
            self.Connect_2(),
            self.Connect_3(),
            self.Connect_4(),
            self.Connect_5(),
            self.Connect_6(),
        )

    # arm 6 drone
    async def arm_6_drone(self):
        await asyncio.gather(
            self.Arming_1(),
            self.Arming_2(),
            self.Arming_3(),
            self.Arming_4(),
            self.Arming_5(),
            self.Arming_6(),
        )

    # takeoff 6 drone
    async def take_off_6_drone(self):
        await asyncio.gather(
            self.Take_off_1(),
            self.Take_off_2(),
            self.Take_off_3(),
            self.Take_off_4(),
            self.Take_off_5(),
            self.Take_off_6(),
        )

    # Land 6 drone
    async def land_6_drone(self):
        await asyncio.gather(
            self.Land_1(),
            self.Land_2(),
            self.Land_3(),
            self.Land_4(),
            self.Land_5(),
            self.Land_6(),
        )

    # Mission 6 drone
    async def mission_all(self):
        await asyncio.gather(
            self.mission_drone_1(),
            self.mission_drone_2(),
            self.mission_drone_3(),
            self.mission_drone_4(),
            self.mission_drone_5(),
        )

    # Upload mission 6 drone
    async def upload_ms_all(self):
        await asyncio.gather(
            self.upload_ms_1(),
            self.upload_ms_2(),
            self.upload_ms_3(),
            self.upload_ms_4(),
            self.upload_ms_5(),
        )

    # Go to 6 drone
    async def goto_all(self):
        await asyncio.gather(
            self.goto_1(),
            self.goto_2(),
            self.goto_3(),
            self.goto_4(),
            self.goto_5(),
            self.goto_6(),
        )

    # RTL 6 drone
    async def RTL_ALL(self):
        await asyncio.gather(
            self.RTL_1(),
            self.RTL_2(),
            self.RTL_3(),
            self.RTL_4(),
            self.RTL_5(),
            self.RTL_6(),
        )

    # Pause mission 6 drone
    async def pause_all(self):
        await asyncio.gather(
            self.pause_1(),
            self.pause_2(),
            self.pause_3(),
            self.pause_4(),
            self.pause_5(),
            self.pause_6(),
        )

    #############################################################################################################################################
    async def detect_object(self):
        await self.test3()
        is_detected = False  # Biến cờ để kiểm soát việc thoát khỏi vòng lặp while
        while not is_detected:  # Lặp cho đến khi phát hiện
            folder_path = f"{parent_dir}/logs/detect"
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name.endswith(".txt"):

                    is_detected = True
                    break  # Thoát khỏi vòng lặp for khi phát hiện được file
            await asyncio.sleep(1)
        # set widget label có tên waiting_connect_1 hiển thị nội dung "Drone1 connected"
        self.ui.label_166.setText("found object!!!")
        self.ui.label_166.setStyleSheet("color: rgb(0,255,0);")  # đổi màu chữ của label
        self.ui.file_all_uav.appendPlainText("found object!!!")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("found object!!!")
        folder_path = f"{parent_dir}/logs/detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split(","))
        self.ui.file_all_uav.appendPlainText("object latitude: " + str(lat_detect))
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "object latitude: " + str(lat_detect)
        )
        self.ui.file_all_uav.appendPlainText("object longitude: " + str(lon_detect))
        self.ui.plainTextEdit_all_6_uav.appendPlainText(
            "object longitude: " + str(lon_detect)
        )
        # uav_goto = float(self.ui.uav_goto.toPlainText())
        await asyncio.gather(
            self.upload_ms_6(),
            self.pause_1(),
            self.pause_2(),
            self.pause_3(),
            self.pause_4(),
            self.pause_5(),
        )
        # await self.compare_distance(self.folders_to_scan)

    async def test3(self):
        subprocess.Popen(["python3", "test3.py"])

    ###############################################################################################################################################
    async def control_camera(self):
        subprocess.Popen(["python3", f"{parent_dir}/App_controlCamera/main.py"])

    ################################################################################################################################################
    async def khoang_cach(self, lat1, lon1, lat2, lon2):
        R = 6378000  # bán kính Trái Đất (đơn vị: m)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
            math.radians(lat1)
        ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    async def compare_distance(self, num_uav):
        if num_uav <= 0:
            return

        folder_path = f"{parent_dir}/logs/detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split(", "))

        drones = [drone_1, drone_2, drone_3, drone_4, drone_5]  # Add all drones here
        drones = drones[:num_uav]  # Filter drones based on num_uav

        latitudes = []
        longitudes = []
        for drone in drones:
            async for position in drone.telemetry.position():
                latitudes.append(position.latitude_deg)
                longitudes.append(position.longitude_deg)
                break

        if not latitudes or not longitudes:
            print("No positions found for any drone.")
            return

        distances = []
        for lat, lon in zip(latitudes, longitudes):
            distance = await self.khoang_cach(lat, lon, lat_detect, lon_detect)
            print(distance)
            distances.append(distance)

        sorted_uavs_index = sorted(range(len(distances)), key=lambda i: distances[i])
        uavs_to_control = sorted_uavs_index[:num_uav]
        await self.goto_alluav(uavs_to_control)

    async def goto_alluav(self, uavs_to_control):
        await asyncio.gather(*[self.goto_drone(index) for index in uavs_to_control])

    async def goto_drone(self, index):
        folder_path = f"{parent_dir}/logs/detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split(", "))

        if index < 0 or index >= 5:
            raise ValueError("Invalid drone index")

        drone = [drone_1, drone_2, drone_3, drone_4, drone_5][index]
        async for position in drone.telemetry.position():
            if (
                abs(position.latitude_deg - lat_detect) < 0.0001
                and abs(position.longitude_deg - lon_detect) < 0.0001
            ):
                print(f"Drone {index+1} is already at the desired location.")
                self.ui.plainTextEdit_all_6_uav.appendPlainText(
                    f"Drone {index+1} is already at the desired location."
                )
                self.ui.file_all_uav.appendPlainText(
                    f"Drone {index+1} is already at the desired location."
                )
                return
            height = position.absolute_altitude_m
            await drone.action.goto_location(lat_detect, lon_detect, height, 0)

    async def button_1_uav_clicked(self):
        # Xử lý khi nút 1 UAV được nhấn
        self.ui.uav_goto.appendPlainText("1")
        await self.compare_distance(1)

    async def button_2_uav_clicked(self):
        # Xử lý khi nút 2 UAV được nhấn
        self.ui.uav_goto.appendPlainText("2")
        await self.compare_distance(2)

    async def button_3_uav_clicked(self):
        # Xử lý khi nút 3 UAV được nhấn
        self.ui.uav_goto.appendPlainText("3")
        await self.compare_distance(3)

    async def button_4_uav_clicked(self):
        # Xử lý khi nút 4 UAV được nhấn
        self.ui.uav_goto.appendPlainText("4")
        await self.compare_distance(4)

    ###################################################################################################################################################
    # Các hàm lấy thông tin

    # Drone 1

    async def get_alt_1(self):
        async for position in drone_1.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav1.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav1.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav1.setText(str(latitude))
            self.ui.longitude_uav1.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data1.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))
        return None

    async def get_mode_1(self):
        async for mode in drone_1.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav1.setText(mod)
        return None

    async def get_batt_1(self):
        async for batt in drone_1.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav1.setText(str(v) + " V")
            self.ui.Batt_Rem_uav1.setText(str(rem) + " %")
        return None

    async def get_arm_1(self):
        async for arm in drone_1.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav1.setText(armed)
        return None

    async def get_gps_1(self):
        async for gps in drone_1.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav1.setText(str(gps_fix))
            self.ui.Sat_Num_uav1.setText(str(sat))

    async def print_status_text_1(self):
        async for status_text in drone_1.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_1.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    # Drone 2
    async def get_alt_2(self):
        async for position in drone_2.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav2.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav2.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav2.setText(str(latitude))
            self.ui.longitude_uav2.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data2.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))

        return None

    async def get_mode_2(self):
        async for mode in drone_2.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav2.setText(mod)
        return None

    async def get_batt_2(self):
        async for batt in drone_2.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav2.setText(str(v) + " V")
            self.ui.Batt_Rem_uav2.setText(str(rem) + " %")
        return None

    async def get_arm_2(self):
        async for arm in drone_2.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav2.setText(armed)
        return None

    async def get_gps_2(self):
        async for gps in drone_2.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav2.setText(str(gps_fix))
            self.ui.Sat_Num_uav2.setText(str(sat))

    async def print_status_text_2(self):
        async for status_text in drone_2.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_2.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    # Drone 3
    async def get_alt_3(self):
        async for position in drone_3.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav3.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav3.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav3.setText(str(latitude))
            self.ui.longitude_uav3.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data3.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))
        return None

    async def get_mode_3(self):
        async for mode in drone_3.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav3.setText(mod)
        return None

    async def get_batt_3(self):
        async for batt in drone_3.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav3.setText(str(v) + " V")
            self.ui.Batt_Rem_uav3.setText(str(rem) + " %")
        return None

    async def get_arm_3(self):
        async for arm in drone_3.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav3.setText(armed)
        return None

    async def get_gps_3(self):
        async for gps in drone_3.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav3.setText(str(gps_fix))
            self.ui.Sat_Num_uav3.setText(str(sat))

    async def print_status_text_3(self):
        async for status_text in drone_3.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_3.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    # Drone 4

    async def get_alt_4(self):
        async for position in drone_4.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav4.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav4.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav4.setText(str(latitude))
            self.ui.longitude_uav4.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data4.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))
        return None

    async def get_mode_4(self):
        async for mode in drone_4.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav4.setText(mod)
        return None

    async def get_batt_4(self):
        async for batt in drone_4.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav4.setText(str(v) + " V")
            self.ui.Batt_Rem_uav4.setText(str(rem) + " %")
        return None

    async def get_arm_4(self):
        async for arm in drone_4.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav4.setText(armed)
        return None

    async def get_gps_4(self):
        async for gps in drone_4.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav4.setText(str(gps_fix))
            self.ui.Sat_Num_uav4.setText(str(sat))

    async def print_status_text_4(self):
        async for status_text in drone_4.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_4.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    # Drone 5
    async def get_alt_5(self):
        async for position in drone_5.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav5.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav5.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav5.setText(str(latitude))
            self.ui.longitude_uav5.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data5.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))
        return None

    async def get_mode_5(self):
        async for mode in drone_5.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav5.setText(mod)
        return None

    async def get_batt_5(self):
        async for batt in drone_5.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav5.setText(str(v) + " V")
            self.ui.Batt_Rem_uav5.setText(str(rem) + " %")
        return None

    async def get_arm_5(self):
        async for arm in drone_5.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav5.setText(armed)
        return None

    async def get_gps_5(self):
        async for gps in drone_5.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav5.setText(str(gps_fix))
            self.ui.Sat_Num_uav5.setText(str(sat))

    async def print_status_text_5(self):
        async for status_text in drone_5.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_5.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    # Drone 6
    async def get_alt_6(self):
        async for position in drone_6.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_uav6.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav6.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav6.setText(str(latitude))
            self.ui.longitude_uav6.setText(str(longitude))
            with open(f"{parent_dir}/logs/gps/gps_data6.txt", "w") as f:
                f.write(str(latitude) + ", " + str(longitude))
        return None

    async def get_mode_6(self):
        async for mode in drone_6.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_uav6.setText(mod)
        return None

    async def get_batt_6(self):
        async for batt in drone_6.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_uav6.setText(str(v) + " V")
            self.ui.Batt_Rem_uav6.setText(str(rem) + " %")
        return None

    async def get_arm_6(self):
        async for arm in drone_6.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_uav6.setText(armed)
        return None

    async def get_gps_6(self):
        async for gps in drone_6.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_uav6.setText(str(gps_fix))
            self.ui.Sat_Num_uav6.setText(str(sat))

    async def print_status_text_6(self):
        async for status_text in drone_6.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.drone_status_6.appendPlainText(Status_Text)
            self.ui.plainTextEdit_all_6_uav.appendPlainText(Status_Text)

    ###################################################################################################################################################
    # Hàm lấy thông tin setup
    async def information_1(self):
        takeoff_altitude_1 = await drone_1.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_1.setText(str(takeoff_altitude_1))
        self.ui.mis_takeoff_alt_change_1.appendPlainText(str(takeoff_altitude_1))
        speed_takeoff_1 = await drone_1.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_1.setText(str(speed_takeoff_1))
        self.ui.mpc_tko_speed_change_1.appendPlainText(str(speed_takeoff_1))
        speed_land_1 = await drone_1.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_1.setText(str(speed_land_1))
        self.ui.mpc_land_speed_change_1.appendPlainText(str(speed_land_1))
        disarm_land_1 = await drone_1.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_1.setText(str(disarm_land_1))
        self.ui.com_disarm_land_change_1.appendPlainText(str(disarm_land_1))

        speed_yaw_1 = await drone_1.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_1.setText(str(speed_yaw_1))
        self.ui.mc_yaw_p_change_1.appendPlainText(str(speed_yaw_1))

    async def information_2(self):
        takeoff_altitude_2 = await drone_2.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_2.setText(str(takeoff_altitude_2))
        self.ui.mis_takeoff_alt_change_2.appendPlainText(str(takeoff_altitude_2))
        speed_takeoff_2 = await drone_2.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_2.setText(str(speed_takeoff_2))
        self.ui.mpc_tko_speed_change_2.appendPlainText(str(speed_takeoff_2))
        speed_land_2 = await drone_2.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_2.setText(str(speed_land_2))
        self.ui.mpc_land_speed_change_2.appendPlainText(str(speed_land_2))
        disarm_land_2 = await drone_2.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_2.setText(str(disarm_land_2))
        self.ui.com_disarm_land_change_2.appendPlainText(str(disarm_land_2))

        speed_yaw_2 = await drone_2.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_2.setText(str(speed_yaw_2))
        self.ui.mc_yaw_p_change_2.appendPlainText(str(speed_yaw_2))

    async def information_3(self):
        takeoff_altitude_3 = await drone_3.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_3.setText(str(takeoff_altitude_3))
        self.ui.mis_takeoff_alt_change_3.appendPlainText(str(takeoff_altitude_3))
        speed_takeoff_3 = await drone_3.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_3.setText(str(speed_takeoff_3))
        self.ui.mpc_tko_speed_change_3.appendPlainText(str(speed_takeoff_3))
        speed_land_3 = await drone_3.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_3.setText(str(speed_land_3))
        disarm_land_3 = await drone_3.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_3.setText(str(disarm_land_3))
        self.ui.com_disarm_land_change_3.appendPlainText(str(disarm_land_3))

        speed_yaw_3 = await drone_3.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_3.setText(str(speed_yaw_3))

    async def information_4(self):
        takeoff_altitude_4 = await drone_4.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_4.setText(str(takeoff_altitude_4))
        speed_takeoff_4 = await drone_4.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_4.setText(str(speed_takeoff_4))
        speed_land_4 = await drone_4.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_4.setText(str(speed_land_4))
        disarm_land_4 = await drone_4.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_4.setText(str(disarm_land_4))

        speed_yaw_4 = await drone_4.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_4.setText(str(speed_yaw_4))

    async def information_5(self):
        takeoff_altitude_5 = await drone_5.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_5.setText(str(takeoff_altitude_5))
        speed_takeoff_5 = await drone_5.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_5.setText(str(speed_takeoff_5))
        speed_land_5 = await drone_5.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_5.setText(str(speed_land_5))
        disarm_land_5 = await drone_5.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_5.setText(str(disarm_land_5))

        speed_yaw_5 = await drone_5.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_5.setText(str(speed_yaw_5))

    async def information_6(self):
        takeoff_altitude_6 = await drone_6.param.get_param_float("MIS_TAKEOFF_ALT")
        self.ui.mis_takeoff_alt_set_6.setText(str(takeoff_altitude_6))
        speed_takeoff_6 = await drone_6.param.get_param_float("MPC_TKO_SPEED")
        self.ui.mpc_tko_speed_set_6.setText(str(speed_takeoff_6))
        speed_land_6 = await drone_6.param.get_param_float("MPC_LAND_SPEED")
        self.ui.mpc_land_speed_set_6.setText(str(speed_land_6))
        disarm_land_6 = await drone_6.param.get_param_float("COM_DISARM_LAND")
        self.ui.com_disarm_land_set_6.setText(str(disarm_land_6))

        speed_yaw_6 = await drone_6.param.get_param_float("MC_YAW_P")
        self.ui.mc_yaw_p_set_6.setText(str(speed_yaw_6))

    ###################################################################################################################################################
    # Hàm chỉnh sửa thông tin
    async def change_information_1(self):
        new_speed_takeoff_1 = float(self.ui.mpc_tko_speed_change_1.toPlainText())
        await drone_1.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_1)
        new_speed_land_1 = float(self.ui.mpc_land_speed_change_1.toPlainText())
        await drone_1.param.set_param_float("MPC_LAND_SPEED", new_speed_land_1)
        new_speed_yaw_1 = float(self.ui.mc_yaw_p_change_1.toPlainText())
        await drone_1.param.set_param_float("MC_YAW_P", new_speed_yaw_1)
        new_com_disarm_land = float(self.ui.com_disarm_land_change_1.toPlainText())
        await drone_1.param.set_param_float("COM_DISARM_LAND", new_com_disarm_land)
        await self.information_1()

    async def change_information_2(self):
        new_speed_takeoff_2 = float(self.ui.mpc_tko_speed_change_2.toPlainText())
        await drone_2.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_2)
        new_speed_land_2 = float(self.ui.mpc_land_speed_change_2.toPlainText())
        await drone_2.param.set_param_float("MPC_LAND_SPEED", new_speed_land_2)
        new_speed_yaw_2 = float(self.ui.mc_yaw_p_change_2.toPlainText())
        await drone_2.param.set_param_float("MC_YAW_P", new_speed_yaw_2)
        await self.information_2()

    async def change_information_3(self):
        new_speed_takeoff_3 = float(self.ui.mpc_tko_speed_change_3.toPlainText())
        await drone_3.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_3)
        new_speed_land_3 = float(self.ui.mpc_land_speed_change_3.toPlainText())
        await drone_3.param.set_param_float("MPC_LAND_SPEED", new_speed_land_3)
        new_speed_yaw_3 = float(self.ui.mc_yaw_p_change_3.toPlainText())
        await drone_3.param.set_param_float("MC_YAW_P", new_speed_yaw_3)
        await self.information_3()

    async def change_information_4(self):
        new_speed_takeoff_4 = float(self.ui.mpc_tko_speed_change_4.toPlainText())
        await drone_4.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_4)
        new_speed_land_4 = float(self.ui.mpc_land_speed_change_4.toPlainText())
        await drone_4.param.set_param_float("MPC_LAND_SPEED", new_speed_land_4)
        new_speed_yaw_4 = float(self.ui.mc_yaw_p_change_4.toPlainText())
        await drone_4.param.set_param_float("MC_YAW_P", new_speed_yaw_4)
        await self.information_4()

    async def change_information_5(self):
        new_speed_takeoff_5 = float(self.ui.mpc_tko_speed_change_5.toPlainText())
        await drone_5.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_5)
        new_speed_land_5 = float(self.ui.mpc_land_speed_change_5.toPlainText())
        await drone_5.param.set_param_float("MPC_LAND_SPEED", new_speed_land_5)
        new_speed_yaw_5 = float(self.ui.mc_yaw_p_change_5.toPlainText())
        await drone_5.param.set_param_float("MC_YAW_P", new_speed_yaw_5)
        await self.information_5()

    async def change_information_6(self):
        new_speed_takeoff_6 = float(self.ui.mpc_tko_speed_change_6.toPlainText())
        await drone_6.param.set_param_float("MPC_TKO_SPEED", new_speed_takeoff_6)
        new_speed_land_6 = float(self.ui.mpc_land_speed_change_6.toPlainText())
        await drone_6.param.set_param_float("MPC_LAND_SPEED", new_speed_land_6)
        new_speed_yaw_6 = float(self.ui.mc_yaw_p_change_6.toPlainText())
        await drone_6.param.set_param_float("MC_YAW_P", new_speed_yaw_6)
        await self.information_6()

    # 3333
    async def all(self):
        await asyncio.gather(
            self.upload_ms_all(), self.detect_object(), self.wait_mission()
        )

    async def wait_mission(self):
        while True:
            if self.wait_upload_misson == 5:
                await self.mission_all()
                break
            await asyncio.sleep(2)

    # 333
    @pyqtSlot(np.ndarray)
    def update_1(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_1.setPixmap(qt_img)

    def update_2(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_2.setPixmap(qt_img)

    def update_3(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_3.setPixmap(qt_img)

    def update_4(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_4.setPixmap(qt_img)

    def update_5(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_5.setPixmap(qt_img)

    def update_6(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.Monitor_drone_6.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        p = convert_to_Qt_format.scaled(
            self.ui.Monitor_drone_1.geometry().width(),
            self.ui.Monitor_drone_1.geometry().height(),
            Qt.KeepAspectRatio,
        )
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        sys.exit(loop.run_forever())
