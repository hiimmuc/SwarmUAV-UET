#Import các thư viện
import asyncio
import json
import math  # Thư viên tính toán để áp dụng tính khoảng cách từ uav đến đối tượng
import os
import subprocess
import sys  # Thư
import time

import cv2
import numpy as np
from asyncqt import QEventLoop, asyncSlot
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsDropShadowEffect,
    QLabel,
    QPushButton,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)

from UI.ui_interface import *  # File giao diện được tạo từ phần mềm Qt5

# from VideoThread import *


# Gán địa chỉ port kết nối cho từng drone thông qua thư viện mavsdk
drone_1 = System(mavsdk_server_address="localhost", port=50060)
drone_2 = System(mavsdk_server_address="localhost", port=50061)
drone_3 = System(mavsdk_server_address="localhost", port=50062)
drone_4 = System(mavsdk_server_address="localhost", port=50063)
drone_5 = System(mavsdk_server_address="localhost", port=50064)
drone_6 = System(mavsdk_server_address="localhost", port=50065)

video_1 = "xx1.mp4"
video_2 = "rtsp://192.168.144.225:8554/main.264"
video_3 = "xx3.mp4"
video_4 = "xx4.mp4"
video_5 = "xx5.mp4"
video_6 = "xx6.mp4"

import time
from datetime import datetime  # lấy thời gian thực
from queue import Queue  # Import Queue để sử dụng frame_queue

from mavsdk.gimbal import Gimbal  # Thêm import cho gimbal
from PyQt5.QtCore import (  # di chuột
    QMutex,
    QPoint,
    Qt,
    QThread,
    QWaitCondition,
    pyqtSignal,
)
from PyQt5.QtGui import QMouseEvent  # chuột
from PyQt5.QtGui import QImage, QPixmap  # Bổ sung import QImage
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from UI.ui_interface import Ui_MainWindow  # Nhập giao diện được thiết kế sẵn

#from ultralytics import YOLO

class VideoThread1(QThread):
    """Thread để xử lý video, phát video và phát tín hiệu hình ảnh."""
    change_pixmap_signal = pyqtSignal(QImage)  # Tín hiệu phát hình ảnh mới đến widget

    def __init__(self, video_path,video_widget, target_fps=20):
        """Khởi tạo VideoThread1 với đường dẫn video và FPS mong muốn."""
        super().__init__()
        self.video_path = video_path  # Đường dẫn video hoặc camera
        self.cap = None  # Khởi tạo capture là None
        self.video_widget = video_widget  # Tham chiếu đến VideoWidget để kiểm tra detecting
        self._run_flag = True  # Cờ để điều khiển việc chạy của thread
        self._paused = False  # Cờ để tạm dừng video
        self.target_fps = target_fps  # Tốc độ khung hình mong muốn
        self.frame_rate = 25  # Tốc độ khung hình mặc định (FPS)
        self.is_camera = isinstance(video_path, int) or str(video_path).isdigit() or video_path.startswith("http")  # Kiểm tra camera
        #self.model = YOLO(r'D:\side menu tutorial (copy)\Qt_By_Du\yolo11n.pt')  # Đường dẫn mô hình YOLO
        self.results = None

    def start_capture(self):
        """Mở video hoặc camera."""
        self.cap = cv2.VideoCapture(self.video_path)  # Mở video
        if self.is_camera:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # Tăng bộ đệm cho stream RTSP

        if not self.cap.isOpened():
            print(f"Error: Unable to open video source {self.video_path}")
            return False
        else:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            if fps > 0:
                self.frame_rate = fps  # Cập nhật FPS thực tế
            return True

    def run(self):
        """Chạy vòng lặp để đọc và phát video."""
        frame_count = 0  # Khởi tạo biến đếm khung hình        
        while self._run_flag:
            if not self.start_capture():  # Cố gắng mở video/camera
                print("Attempting to reconnect...")
                self.msleep(1000)  # Đợi một giây trước khi thử lại
                continue  # Tiếp tục thử kết nối lại

            while self._run_flag:
                if self._paused:  # Kiểm tra nếu đang tạm dừng
                    self.msleep(50)  # Sử dụng msleep để tránh lag giao diện
                    continue

                start_time = time.time()  # Ghi lại thời gian bắt đầu
                ret, frame = self.cap.read()  # Đọc khung hình từ video

                if ret:  # Nếu đọc khung hình thành công
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi khung hình từ BGR sang RGB
                    frame_resized = cv2.resize(frame, (480, 320), interpolation=cv2.INTER_LINEAR)  # Giảm độ phân giải cho khung hình
                    frame_count += 1  # Tăng biến đếm khung hình
                    if self.video_widget.detecting and frame_count % 5 == 0:
                        self.results = self.model(frame_resized)  # Nhận diện người bằng mô hình YOLO
                    elif not self.video_widget.detecting:
                        self.results = None  # Xóa kết quả nhận diện khi tắt chế độ detect

                    

                    # Vẽ các hộp giới hạn và nhãn lên khung hình
                    if self.results :
                        for result in self.results:
                            boxes = result.boxes.xyxy  # Tọa độ hộp giới hạn
                            scores = result.boxes.conf  # Điểm số tin cậy
                            labels = result.boxes.cls  # Nhãn

                            for box, score, label in zip(boxes, scores, labels):
                                if label == 0 and score > 0.5:  # Nhãn '0' thường đại diện cho người
                                    x1, y1, x2, y2 = map(int, box)
                                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Vẽ hộp giới hạn màu xanh lá
                                    cv2.putText(frame_resized, f'person: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                                elif label == 1 and score > 0.5:  # Nhãn '0' thường đại diện cho người
                                    x1, y1, x2, y2 = map(int, box)
                                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Vẽ hộp giới hạn màu xanh lá
                                    cv2.putText(frame_resized, f'bike: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                                elif label == 2 and score > 0.5:  # Nhãn '0' thường đại diện cho người
                                    x1, y1, x2, y2 = map(int, box)
                                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Vẽ hộp giới hạn màu xanh lá
                                    cv2.putText(frame_resized, f'car: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Chuyển đổi khung hình từ numpy sang QImage để hiển thị
                    h, w, ch = frame_resized.shape
                    bytes_per_line = ch * w
                    convert_to_qt_format = QImage(frame_resized.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    self.change_pixmap_signal.emit(convert_to_qt_format)  # Phát tín hiệu với khung hình

                    # Điều chỉnh thời gian ngủ để đồng bộ với tốc độ FPS
                    elapsed_time = time.time() - start_time  # Tính thời gian đã trôi qua
                    wait_time = max(0, (1.0 / self.target_fps) - elapsed_time)  # Tính toán thời gian cần ngủ
                    self.msleep(int(wait_time * 1000))  # Điều chỉnh thời gian ngủ
                else: # nếu mất kết nối quay lại dòng 83 chạy lại hàm kết nối lại
                    print("Frame not received or corrupt, skipping...")  # Nếu không nhận được khung hình
                    self.msleep(1000)  # Chờ một chút rồi thử lại
                    self.cap.release()  # Giải phóng tài nguyên video
                    break

            # Nếu thoát khỏi vòng lặp đọc khung hình, giải phóng tài nguyên
            if self.cap is not None:
                self.cap.release()  # Giải phóng tài nguyên video
    def stop(self):
        """Dừng thread video."""
        self._run_flag = False
        self.wait()

    def pause(self):
        """Tạm dừng video."""
        self._paused = True

    def resume(self):
        """Tiếp tục phát video."""
        self._paused = False
        if not self.isRunning():
            self.start()

class CaptureThread(QThread):
    """Luồng để xử lý chụp ảnh bất đồng bộ."""
    captured_signal = pyqtSignal(str)

    def __init__(self, image):
        super().__init__()
        self.image = image

    def run(self):
        """Thực hiện chụp ảnh và lưu thành file."""
        if self.image is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(os.path.dirname(__file__), "anh", f"captured_image_{timestamp}.png")
            if self.image.save(save_path):
                self.captured_signal.emit(f"Ảnh đã được lưu tại {save_path}")
            else:
                self.captured_signal.emit("Lỗi: Không thể lưu ảnh.")
        else:
            self.captured_signal.emit("Không có khung hình để chụp.")

class RecordThread(QThread):
    """Luồng để ghi video."""
    def __init__(self, video_writer, frame_queue):
        super().__init__()
        self.video_writer = video_writer
        self.frame_queue = frame_queue
        self.running = True

    def run(self):
        """Ghi khung hình vào video liên tục."""
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()  # Lấy khung hình từ hàng đợi
                if frame is not None and self.video_writer is not None:
                    # Ghi khung hình và kiểm tra nếu đã đạt tốc độ ghi
                    try:
                        self.video_writer.write(frame)
                    except Exception as e:
                        print(f"Lỗi khi ghi khung hình: {e}")

            # Thêm độ trễ nhỏ nếu cần để kiểm soát tốc độ ghi
            time.sleep(0.01)  # Điều chỉnh độ trễ nếu cần

    def stop(self):
        """Dừng ghi video."""
        self.running = False
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

class VideoWidget(QWidget):
    """Widget để hiển thị video trong giao diện người dùng."""
    def __init__(self, video_label: QLabel, start_button: QPushButton, stop_button: QPushButton, zoom1_button: QPushButton, zoom0_button: QPushButton, cap_button: QPushButton, record_button: QPushButton,detect_button: QPushButton, video_path: str):
        super().__init__()
        self.video_label = video_label
        self.start_button = start_button
        self.stop_button = stop_button
        self.zoom1_button = zoom1_button
        self.zoom0_button = zoom0_button
        self.cap_button = cap_button
        self.record_button = record_button
        self.detect_button = detect_button
        self.video_path = video_path
        self.thread = None
        self.zoom_scale = 1.0
        self.last_image = None
        self.offset = QPoint(0, 0)
        self.dragging = False
        self.previous_pos = QPoint(0, 0)
        self.scaled_pixmap = None
        self.recording = False
        self.video_writer = None
        self.frame_queue = Queue(maxsize=10)  # Khởi tạo frame_queue để lưu khung hình
        self.detecting = False  # Biến kiểm soát trạng thái phát hiện

        self.save_folder = os.path.join(os.path.dirname(__file__), 'anh')
        os.makedirs(self.save_folder, exist_ok=True)  # Tạo thư mục 'anh' nếu chưa tồn tại

        self.start_button.clicked.connect(self.start_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.zoom1_button.clicked.connect(self.zoom_in)
        self.zoom0_button.clicked.connect(self.zoom_out)
        self.cap_button.clicked.connect(self.capture_image)
        self.record_button.clicked.connect(self.toggle_recording)
        self.detect_button.clicked.connect(self.toggle_detecting)

        self.video_label.mousePressEvent = self.mouse_press_event
        self.video_label.mouseMoveEvent = self.mouse_move_event
        self.video_label.setMouseTracking(True)

    def start_video(self):
        """Bắt đầu phát video."""
        if self.thread is None or not self.thread.isRunning():
            self.thread = VideoThread1(self.video_path, self)  # Truyền self vào VideoThread1
            self.thread.change_pixmap_signal.connect(self.update_image, Qt.QueuedConnection)
            self.thread.start()

    def stop_video(self):
        """Dừng phát video và xóa nhãn."""
        if self.thread is not None and self.thread.isRunning():
            self.thread.change_pixmap_signal.disconnect()
            self.thread.stop()
            self.thread.wait()
            self.video_label.clear()
            self.thread = None

        if self.recording:
            self.toggle_recording()

    def toggle_detecting(self):
        """Bật hoặc tắt phát hiện hình ảnh."""
        self.detecting = not self.detecting
        if self.detecting:
            self.detect_button.setText("Stop Detect")
            print("Detection started.")
        else:
            self.detect_button.setText("Detect")
            print("Detection stopped.")

    def capture_image(self):
        """Chụp ảnh từ khung hình hiện tại và lưu thành tệp."""
        if self.last_image is not None:
            # Tạo luồng chụp ảnh để không làm khựng video
            self.capture_thread = CaptureThread(self.last_image)
            self.capture_thread.captured_signal.connect(self.on_captured)
            self.capture_thread.start()  # Bắt đầu luồng chụp ảnh
        else:
            print("Không có khung hình để chụp.")

    def on_captured(self, message):
        """Xử lý tín hiệu sau khi chụp ảnh."""
        print(message)  # Hiển thị thông báo lưu ảnh thành công hoặc lỗi

    def zoom_in(self):
        """Phóng to video."""
        if self.last_image is not None:
            self.zoom_scale *= 1.2
            self.update_image(self.last_image)

    def zoom_out(self):
        """Thu nhỏ video."""
        if self.last_image is not None:
            self.zoom_scale *= 0.8
            if self.zoom_scale < 1.0:
                self.zoom_scale = 1.0
            self.update_image(self.last_image)

    def update_image(self, image: QImage):
        """Cập nhật hình ảnh video vào label."""
        if image is None:
            return

        self.last_image = image
        pixmap = QPixmap.fromImage(image)
        new_width = int(pixmap.width() * self.zoom_scale)
        new_height = int(pixmap.height() * self.zoom_scale)
        self.scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        label_size = self.video_label.size()
        offset_x = max(0, (new_width - label_size.width()) // 2)
        offset_y = max(0, (new_height - label_size.height()) // 2)

        display_x = max(0, min(self.offset.x() + offset_x, new_width - label_size.width()))
        display_y = max(0, min(self.offset.y() + offset_y, new_height - label_size.height()))

        self.video_label.setPixmap(self.scaled_pixmap.copy(display_x, display_y, label_size.width(), label_size.height()))

        # Chuyển QImage sang định dạng OpenCV và thêm vào frame_queue
        frame = self.convert_qimage_to_frame(image)
        if not self.frame_queue.full():
            self.frame_queue.put(frame)

    def convert_qimage_to_frame(self, qimage):
        """Chuyển đổi QImage thành khung hình."""
        buffer = qimage.bits()
        buffer.setsize(qimage.byteCount())
        frame = np.array(buffer).reshape((qimage.height(), qimage.width(), 3))
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def mouse_press_event(self, event):
        """Xử lý sự kiện nhấn chuột để kéo video."""
        if event.button() == Qt.LeftButton:
            self.previous_pos = event.pos()
            self.dragging = True

    def mouse_move_event(self, event):
        """Xử lý sự kiện di chuyển chuột để kéo video."""
        if self.dragging:
            delta = event.pos() - self.previous_pos
            self.previous_pos = event.pos()
            self.offset += delta
            self.update_image(self.last_image)

    def toggle_recording(self):
        """Bật hoặc tắt ghi video."""
        if self.recording:
            self.recording = False
            self.record_thread.stop()  # Dừng luồng ghi
            self.record_thread.wait()
            self.video_writer.release()
            self.video_writer = None
            self.record_button.setText("Bắt đầu ghi")  # Đổi văn bản nút
            print("Dừng ghi video.")
        else:
            self.recording = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.save_folder, f"recorded_video_{timestamp}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Đổi mã nén sang 'mp4v' cho định dạng .
            self.video_writer = cv2.VideoWriter(save_path, fourcc, 20, (480, 320))
            self.record_thread = RecordThread(self.video_writer, self.frame_queue)  # Truyền frame_queue vào
            self.record_thread.start()
            self.record_button.setText("Dừng ghi")  # Đổi văn bản nút
            print(f"Bắt đầu ghi video tại {save_path}")

    """def stop_recording(self):

        if self.recording:
            self.recording = False
            if self.record_thread is not None:
                self.record_thread.stop()
                self.record_thread.wait()
                self.record_thread = None
            print("Recording stopped.")
    """

    """def update_image(self, image: QImage):
        
        if image is None:  # Kiểm tra nếu khung hình bị None
            return  # Không làm gì cả nếu khung hình là None

        self.last_image = image  # Lưu lại khung hình cuối cùng
        pixmap = QPixmap.fromImage(image)  # Chuyển đổi QImage thành QPixmap

        # Cập nhật pixmap vào label với kích thước có tính đến tỷ lệ zoom
        scaled_pixmap = pixmap.scaled(self.video_label.size() * self.zoom_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        self.video_label.setPixmap(scaled_pixmap)  # Đặt pixmap vào label"""
    """def update_image(self, image: QImage):
        
        pixmap = QPixmap.fromImage(image)  # Chuyển đổi QImage thành QPixmap
        # Cập nhật pixmap vào label mà không thay đổi kích thước của label
        scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        self.video_label.setPixmap(scaled_pixmap)  # Đặt pixmap vào label
        """
    """def update_image(self, image: QImage):

        if image is None:
            return

        self.last_image = image  # Lưu khung hình cuối cùng
        pixmap = QPixmap.fromImage(image)  # Chuyển QImage thành QPixmap

        # Kích thước gốc của khung hình
        video_size = pixmap.size()

        # Kích thước sau khi zoom
        new_width = int(video_size.width() * self.zoom_scale)
        new_height = int(video_size.height() * self.zoom_scale)

        # Phóng to hoặc thu nhỏ QPixmap
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Cắt hoặc thêm khoảng trống để vừa khít với QLabel mà không thay đổi kích thước QLabel
        label_size = self.video_label.size()

        if new_width > label_size.width() or new_height > label_size.height():
            # Nếu video lớn hơn QLabel, cắt bớt phần thừa
            scaled_pixmap = scaled_pixmap.copy(
                (new_width - label_size.width()) // 2,
                (new_height - label_size.height()) // 2,
                label_size.width(),
                label_size.height()
            )

        # Đặt pixmap đã phóng to/thu nhỏ vào label mà không thay đổi kích thước label
        self.video_label.setPixmap(scaled_pixmap)"""




## điều khiển gimbal

## điều khiển gimbal
class GimbalControllerIndividual:
    """Lớp điều khiển gimbal của từng drone."""
    def __init__(self, drone: System, system_address: str):
        self.drone = drone
        self.system_address = system_address
        self.connected = False
        self.current_pitch = 0
        self.current_yaw = 0
        self.gimbal_connected = False

    async def connect(self):
        """Kết nối với drone."""
        try:
            await self.drone.connect(system_address=self.system_address)
            self.connected = True
            print(f"Kết nối với drone tại {self.system_address} thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối với drone tại {self.system_address}: {e}. Đang thử lại...")
            await asyncio.sleep(2)  # Chờ 2 giây trước khi thử lại
            await self.connect()  # Thử lại kết nối

    async def connect_gimbal(self):
        """Kết nối với gimbal và kiểm tra trạng thái."""
        if self.connected:
            try:
                async for control_result in self.drone.gimbal.control():
                    print("Gimbal đã kết nối thành công.")
                    await asyncio.sleep(2)  # Chờ gimbal sẵn sàng
                    try:
                        await asyncio.wait_for(self.drone.gimbal.set_angles(0, 0, 0), timeout=5)  # Giới hạn thời gian chờ 5 giây
                        print("Gimbal đã di chuyển.")
                        self.gimbal_connected = True
                    except asyncio.TimeoutError:
                        print("Timeout khi gửi lệnh điều khiển gimbal.")
                    break
            except Exception as e:
                print(f"Gimbal không thể kết nối: {e}")
        else:
            print("Drone chưa kết nối, không thể kết nối gimbal.")

    async def pitch_up(self):
        """Tăng pitch của gimbal."""
        if self.gimbal_connected:
            new_pitch = min(self.current_pitch + 10, 45)
            await self.drone.gimbal.set_angles(new_pitch, self.current_yaw, 0)
            self.current_pitch = new_pitch
            print(f"Pitch đã tăng lên: {new_pitch} độ")
        else:
            print("Gimbal chưa được kết nối.")

    async def pitch_down(self):
        """Giảm pitch của gimbal."""
        if self.gimbal_connected:
            new_pitch = max(self.current_pitch - 10, -135)
            await self.drone.gimbal.set_angles(new_pitch, self.current_yaw, 0)
            self.current_pitch = new_pitch
            print(f"Pitch đã giảm xuống: {new_pitch} độ")
        else:
            print("Gimbal chưa được kết nối.")

    async def yaw_up(self):
        """Tăng yaw của gimbal."""
        if self.gimbal_connected:
            new_yaw = min(self.current_yaw + 10, 160)
            await self.drone.gimbal.set_angles(self.current_pitch, new_yaw, 0)
            self.current_yaw = new_yaw
            print(f"Yaw đã tăng lên: {new_yaw} độ")
        else:
            print("Gimbal chưa được kết nối.")

    async def yaw_down(self):
        """Giảm yaw của gimbal."""
        if self.gimbal_connected:
            new_yaw = max(self.current_yaw - 10, -160)
            await self.drone.gimbal.set_angles(self.current_pitch, new_yaw, 0)
            self.current_yaw = new_yaw
            print(f"Yaw đã giảm xuống: {new_yaw} độ")
        else:
            print("Gimbal chưa được kết nối.")


class GimbalController:
    """Lớp điều khiển gimbal cho toàn bộ drone."""
    def __init__(self, ui):
        self.ui = ui
        self.gimbal_controllers = []
        system_addresses = ["udp://:14540", "udp://:14541", "udp://:14542", "udp://:14543", "udp://:14544", "udp://:14545"]
        
        for i, system_address in enumerate(system_addresses):
            drone = System(mavsdk_server_address="localhost", port=50060 + i)
            gimbal_controller = GimbalControllerIndividual(drone, system_address)
            self.gimbal_controllers.append(gimbal_controller)

        self.setup_button_connections()

    def setup_button_connections(self):
        """Kết nối các nút điều khiển của từng drone."""
        for i in range(6):
            self.ui.__getattribute__(f'pitch_up{i+1}').clicked.connect(lambda _, c=self.gimbal_controllers[i]: asyncio.ensure_future(c.pitch_up()))
            self.ui.__getattribute__(f'pitch_down{i+1}').clicked.connect(lambda _, c=self.gimbal_controllers[i]: asyncio.ensure_future(c.pitch_down()))
            self.ui.__getattribute__(f'yaw_up{i+1}').clicked.connect(lambda _, c=self.gimbal_controllers[i]: asyncio.ensure_future(c.yaw_up()))
            self.ui.__getattribute__(f'yaw_down{i+1}').clicked.connect(lambda _, c=self.gimbal_controllers[i]: asyncio.ensure_future(c.yaw_down()))

            



# Khi sử dụng lớp này, bạn sẽ khởi tạo VideoWidget với QLabel, nút bắt đầu và dừng, và đường dẫn tới video.
class MainWindow(QMainWindow): # Class giao diện MainWindow, nó kế thừa từ lớp (QMainWindown)>> MainWindow là một lớp con của QMainWindown và kế thừa các thuộc tính và phương thức từ QMainWindown.
    '''Khởi tạo'''
    async def connect_drones(self):
        """Kết nối với các drone và khởi tạo gimbal."""
        for controller in self.gimbal_controller.gimbal_controllers:
            await controller.connect()
            await controller.connect_gimbal()
            await asyncio.sleep(0.1)  # Đặt độ trễ nhỏ để tránh quá tải
    def __init__(self): # Định nghĩa phương thức __init__
        QMainWindow.__init__(self) 
        self.ui = Ui_MainWindow() # Tạo một đối tượng của lớp Ui_MainWindow và gán nó cho thuộc tính ui của đối tượng hiện tại
        
        self.ui.setupUi(self)   # Gọi phương thức setupUi của đối tượng ui (được tạo từ lớp Ui_MainWindow) và truyền đối tượng hiện tại (self) vào làm đối số

        self.wait_upload_misson = 0
        self.ui.start.clicked.connect(lambda: asyncio.create_task(self.all()))
        """Window contain Video"""
        # create the video capture thread
        #self.thread_1 = VideoThread(0, video_1)
       
        # self.thread_2 = VideoThread(1, video_2)
        # self.thread_3 = VideoThread(2, video_3)
        # self.thread_4 = VideoThread(3, video_4)
        # self.thread_5 = VideoThread(4, video_5)
        # self.thread_6 = VideoThread(5, video_6)
        
        # start the thread
        #self.thread_1.start()
       
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
        
 # Các video path
        video_paths = [0, 'Thermal_video_raw.mp4', 'rtsp://192.168.144.101:8554/main.264', 'rtsp://192.168.144.225:8554/main.264', 'rtsp://192.168.144.225:8554/main.264', 'rtsp://192.168.144.225:8554/main.264']


        # Kết nối các QLabel và QPushButton với chức năng
        self.videos = [
            VideoWidget(self.ui.video1, self.ui.startvd1, self.ui.stopvd1,self.ui.zoom1_vd1, self.ui.zoom0_vd1,self.ui.capvd1,self.ui.recordvd1,self.ui.xlanh1, video_paths[0]),
            VideoWidget(self.ui.video2, self.ui.startvd2, self.ui.stopvd2,self.ui.zoom1_vd2, self.ui.zoom0_vd2,self.ui.capvd2,self.ui.recordvd2,self.ui.xlanh2, video_paths[1]),
            VideoWidget(self.ui.video3, self.ui.startvd3, self.ui.stopvd3,self.ui.zoom1_vd3, self.ui.zoom0_vd3,self.ui.capvd3,self.ui.recordvd3,self.ui.xlanh3, video_paths[2]),
            VideoWidget(self.ui.video4, self.ui.startvd4, self.ui.stopvd4,self.ui.zoom1_vd4, self.ui.zoom0_vd4,self.ui.capvd4,self.ui.recordvd4,self.ui.xlanh4, video_paths[3]),
            VideoWidget(self.ui.video5, self.ui.startvd5, self.ui.stopvd5,self.ui.zoom1_vd5, self.ui.zoom0_vd5,self.ui.capvd5,self.ui.recordvd5,self.ui.xlanh5, video_paths[4]),
            VideoWidget(self.ui.video6, self.ui.startvd6, self.ui.stopvd6,self.ui.zoom1_vd6, self.ui.zoom0_vd6,self.ui.capvd6,self.ui.recordvd6,self.ui.xlanh6, video_paths[5])
        ]

        # Khởi tạo lớp điều khiển gimbal với giao diện
        self.gimbal_controller = GimbalController(self.ui)
        asyncio.ensure_future(self.connect_drones())






    

        ##########################################################################################################################################################
        #Tạo biến toàn cục để kiểm tra xem có bao nhiêu con đã kết nối
        self.number_drone = 0
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))

        with open("ID_drone.txt", "r") as file:# Đọc nội dung của file
             lines = file.readlines()  # Đọc tất cả các dòng trong file

        with open("ID_drone.txt", "w") as file:# Ghi đè nội dung của file với chuỗi trống
             file.write("")  # Xóa nội dung hiện tại của file


        '''Điều khiển từng drone'''
        # Khối code connect từng drone
        self.ui.connect_drone_1.clicked.connect(lambda: asyncio.create_task(self.Connect_1())) # Khi nút connect_drone_1 được nhấn thì gọi đến hàm Connect_1() để kết nốt với uav thông qua các port
        self.ui.connect_drone_2.clicked.connect(lambda: asyncio.create_task(self.Connect_2()))
        self.ui.connect_drone_3.clicked.connect(lambda: asyncio.create_task(self.Connect_3()))
        self.ui.connect_drone_4.clicked.connect(lambda: asyncio.create_task(self.Connect_4()))
        self.ui.connect_drone_5.clicked.connect(lambda: asyncio.create_task(self.Connect_5()))
        self.ui.connect_drone_6.clicked.connect(lambda: asyncio.create_task(self.Connect_6()))
        
        # Khối code arm từng drone, đây là hàm kiểm tra an toàn trước khi bay
        self.ui.arm_drone_1.clicked.connect(lambda: asyncio.create_task(self.Arming_1())) #Khi nút arm_drone_1 được nhấn thì gọi đến hàm Arming_1() để thực hiện lệnh kiểm tra an toàn trước khi bay
        self.ui.arm_drone_2.clicked.connect(lambda: asyncio.create_task(self.Arming_2()))
        self.ui.arm_drone_3.clicked.connect(lambda: asyncio.create_task(self.Arming_3()))
        self.ui.arm_drone_4.clicked.connect(lambda: asyncio.create_task(self.Arming_4()))
        self.ui.arm_drone_5.clicked.connect(lambda: asyncio.create_task(self.Arming_5()))
        self.ui.arm_drone_6.clicked.connect(lambda: asyncio.create_task(self.Arming_6()))

        #Khối code disarm từng drone, đây là hàm kết thúc kiểm tra an toàn
        self.ui.disarm_drone_1.clicked.connect(lambda: asyncio.create_task(self.Disarm_1())) #Khi nút disarm_drone_1 được nhấn thì gọi đến hàm Disarm_1() để thực hiện lệnh kết thúc kiểm tra an toàn trước khi bay
        self.ui.disarm_drone_2.clicked.connect(lambda: asyncio.create_task(self.Disarm_2()))
        self.ui.disarm_drone_3.clicked.connect(lambda: asyncio.create_task(self.Disarm_3()))
        self.ui.disarm_drone_4.clicked.connect(lambda: asyncio.create_task(self.Disarm_4()))
        self.ui.disarm_drone_5.clicked.connect(lambda: asyncio.create_task(self.Disarm_5()))
        self.ui.disarm_drone_6.clicked.connect(lambda: asyncio.create_task(self.Disarm_6()))

        # Khối code takeoff từng drone, đây là hàm cất cánh từng drone 
        self.ui.take_off_drone_1.clicked.connect(lambda: asyncio.create_task(self.Take_off_1())) #Khi nút take_off_drone_1 được nhấn thì gọi đến hàm Take_off_1() để thực hiện lệnh cất cánh
        self.ui.take_off_drone_2.clicked.connect(lambda: asyncio.create_task(self.Take_off_2()))
        self.ui.take_off_drone_3.clicked.connect(lambda: asyncio.create_task(self.Take_off_3()))
        self.ui.take_off_drone_4.clicked.connect(lambda: asyncio.create_task(self.Take_off_4()))
        self.ui.take_off_drone_5.clicked.connect(lambda: asyncio.create_task(self.Take_off_5()))
        self.ui.take_off_drone_6.clicked.connect(lambda: asyncio.create_task(self.Take_off_6()))

        # Khối code land từng drone, đây là hàm hạ cánh từng drone
        self.ui.land_drone_1.clicked.connect(lambda: asyncio.create_task(self.Land_1())) #Khi nút land_drone_1 được nhấn thì gọi đến hàm Land_1() để thực hiện lệnh hạ cánh
        self.ui.land_drone_2.clicked.connect(lambda: asyncio.create_task(self.Land_2()))
        self.ui.land_drone_3.clicked.connect(lambda: asyncio.create_task(self.Land_3()))
        self.ui.land_drone_4.clicked.connect(lambda: asyncio.create_task(self.Land_4()))
        self.ui.land_drone_5.clicked.connect(lambda: asyncio.create_task(self.Land_5()))
        self.ui.land_drone_6.clicked.connect(lambda: asyncio.create_task(self.Land_6()))

        self.ui.return_and_land_drone_1.clicked.connect(lambda: asyncio.create_task(self.RTL_1())) #Khi nút land_drone_1 được nhấn thì gọi đến hàm Land_1() để thực hiện lệnh hạ cánh
        self.ui.return_and_land_drone_2.clicked.connect(lambda: asyncio.create_task(self.RTL_2()))
        self.ui.return_and_land_drone_3.clicked.connect(lambda: asyncio.create_task(self.RTL_3()))
        self.ui.return_and_land_drone_4.clicked.connect(lambda: asyncio.create_task(self.RTL_4()))
        self.ui.return_and_land_drone_5.clicked.connect(lambda: asyncio.create_task(self.RTL_5()))
        self.ui.return_and_land_drone_6.clicked.connect(lambda: asyncio.create_task(self.RTL_6()))

        # Tạo biến toàn cục filename để liên kết giữa file nhiệm vụ được chọn và file để upload trong hàm nhiệm vụ
        self.filename_1 = None
        self.filename_2 = None
        self.filename_3 = None
        self.filename_4 = None
        self.filename_5 = None
        self.filename_6 = None
        
        # Khối code tải nhiệm vụ lên cho từng con một
        self.ui.Load_MS_1.clicked.connect(lambda: asyncio.create_task(self.upload_ms_1()))
        self.ui.Load_MS_2.clicked.connect(lambda: asyncio.create_task(self.upload_ms_2()))
        self.ui.Load_MS_3.clicked.connect(lambda: asyncio.create_task(self.upload_ms_3()))
        self.ui.Load_MS_4.clicked.connect(lambda: asyncio.create_task(self.upload_ms_4()))
        self.ui.Load_MS_5.clicked.connect(lambda: asyncio.create_task(self.upload_ms_5()))
        self.ui.Load_MS_6.clicked.connect(lambda: asyncio.create_task(self.upload_ms_6()))

        # Khối code mission từng drone, đây là hàm ra lệnh bắt đầu thực hiện nhiệm vụ cho từng drone
        self.ui.mission_uav1.clicked.connect(lambda: asyncio.create_task(self.mission_drone_1())) #Khi nút mision_uav_1 được nhấn thì gọi đến hàm mision_drone_1() để thực hiện lệnh bắt đầu nhiệm vụ
        self.ui.mission_uav2.clicked.connect(lambda: asyncio.create_task(self.mission_drone_2()))
        self.ui.mission_uav3.clicked.connect(lambda: asyncio.create_task(self.mission_drone_3()))
        self.ui.mission_uav4.clicked.connect(lambda: asyncio.create_task(self.mission_drone_4()))
        self.ui.mission_uav5.clicked.connect(lambda: asyncio.create_task(self.mission_drone_5()))
        self.ui.mission_uav6.clicked.connect(lambda: asyncio.create_task(self.mission_drone_6()))
        
        # Khối code ra lệnh cho từng con đến vị trí được chỉ định (kinh độ, vĩ độ)
        self.ui.goto_1.clicked.connect(lambda: asyncio.create_task(self.goto_1())) #Khi nút goto_1 được nhấn thì gọi đến hàm goto_1() để thực hiện lệnh cho uav đến vị trí được chỉ định
        self.ui.goto_2.clicked.connect(lambda: asyncio.create_task(self.goto_2()))
        self.ui.goto_3.clicked.connect(lambda: asyncio.create_task(self.goto_3()))
        self.ui.goto_4.clicked.connect(lambda: asyncio.create_task(self.goto_4()))
        self.ui.goto_5.clicked.connect(lambda: asyncio.create_task(self.goto_5()))
        self.ui.goto_6.clicked.connect(lambda: asyncio.create_task(self.goto_6()))

        # Khối code ra lệnh tạm dừng nhiệm vụ cho từng drone
        self.ui.pause_1.clicked.connect(lambda: asyncio.create_task(self.pause_1())) #Khi nút pause_1 được nhấn thì gọi đến hàm pause_1() để thực hiện lệnh UAV1 tạm dừng nhiệm vụ 
        self.ui.pause_2.clicked.connect(lambda: asyncio.create_task(self.pause_2()))
        self.ui.pause_3.clicked.connect(lambda: asyncio.create_task(self.pause_3()))
        self.ui.pause_4.clicked.connect(lambda: asyncio.create_task(self.pause_4()))
        self.ui.pause_5.clicked.connect(lambda: asyncio.create_task(self.pause_5()))
        self.ui.pause_6.clicked.connect(lambda: asyncio.create_task(self.pause_6()))

        # Khi nút pushButton_3 được nhấn thì ta sẽ tiến hành gọi đến hàm photo_and_distance để khởi động quá trình detect bằng cách gọi đến code test3
        self.ui.pushButton_3.clicked.connect(lambda: asyncio.create_task(self.detect_object()))

        # Khi nút pushButton_4 được nhấn thì gọi đến hàm control_camera để mở code điều khiển camera trên drone
        self.ui.pushButton_4.clicked.connect(lambda: asyncio.create_task(self.control_camera()))

        # Khối code ra kệnh cho các uav gần nhất bay đến
        self.ui.fly_1_uav.clicked.connect(lambda: asyncio.create_task(self.button_1_uav_clicked()))# Khi nhấn fly_1_uav thì gọi đến hàm button_1_uav để điều khiển một uav gần nhất đến tọa độ đối tượng
        self.ui.fly_2_uav.clicked.connect(lambda: asyncio.create_task(self.button_2_uav_clicked()))
        self.ui.fly_3_UAV.clicked.connect(lambda: asyncio.create_task(self.button_3_uav_clicked()))
        self.ui.fly_4_UAV.clicked.connect(lambda: asyncio.create_task(self.button_4_uav_clicked()))
    
        # Map
        self.ui.btn_map_all.clicked.connect(lambda: asyncio.create_task(self.open_map())) #Khi nút btn_map_all được nhấn thì gọi đến hàm open_map() để thực hiện mở map bản đồ

        # Khối code lưu các tham số thay đổi
        self.ui.save_1.clicked.connect(lambda: asyncio.create_task(self.change_information_1())) #Khi nút save_1 được nhấn thì gọi đến hàm change_information_1 để thực hiện lệnh lưu các tham số thay đổi
        self.ui.save_2.clicked.connect(lambda: asyncio.create_task(self.change_information_2()))
        self.ui.save_3.clicked.connect(lambda: asyncio.create_task(self.change_information_3()))

        # Khởi tạo QTimer để cập nhật hình ảnh từ thư mục
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.timer4 = QTimer()
        self.timer5 = QTimer()
        #self.timer6 = QTimer(self)

        # Đặt thời gian quét thư mục
        self.timer1.start(1000)  # Sau 1s sẽ tiến hành quét thư viện hình ảnh trong file hung/xx1 một lần để cập nhật ảnh mới nhất lên giao diện
        self.timer2.start(1000)  
        self.timer3.start(1000)  
        self.timer4.start(1000)  
        self.timer5.start(1000)  
        #self.timer6.start(1000)

        # Sau 1s nếu trong file hung/xx1->xx6 nếu có ảnh mới thì sẽ gọi đến hàm update để tiến hành cập nhật
        self.timer1.timeout.connect(self.update_image1)
        self.timer2.timeout.connect(self.update_image2)
        self.timer3.timeout.connect(self.update_image3)
        self.timer4.timeout.connect(self.update_image4)
        self.timer5.timeout.connect(self.update_image5)
        #self.timer6.timeout.connect(self.update_image6)
         
        # Thư mục chứa các tệp hình ảnh để sử dụng trong các hàm update_image1->6
        self.image_directory1 = "./hung/xx1"
        self.image_directory2 = "./hung/xx2"
        self.image_directory3 = "./hung/xx3"
        self.image_directory4 = "./hung/xx4"
        self.image_directory5 = "./hung/xx5"
        self.image_directory6 = "./hung/xx6"

        # Tạo danh sách các tệp hình ảnh để sử dụng trong các hàm update_image1->6
        self.image_files1 = []
        self.image_files2 = []
        self.image_files3 = []
        self.image_files4 = []
        self.image_files5 = []
        self.image_files6 = []


        ##################################################################################################################################################
        '''Control 6 drone'''
        #connect multidrone
        self.ui.connect_all.clicked.connect(lambda: asyncio.create_task(self.connect_6_drone()))

        #takeoff multi drone
        self.ui.take_off_all.clicked.connect(lambda: asyncio.create_task(self.take_off_6_drone()))
        
        #arm multi drone
        self.ui.arm_all.clicked.connect(lambda: asyncio.create_task(self.arm_6_drone()))

        #land multi drone
        self.ui.land_all.clicked.connect(lambda: asyncio.create_task(self.land_6_drone()))

        #Return to land multi drone
        self.ui.RTL_all_2.clicked.connect(lambda: asyncio.create_task(self.RTL_ALL()))

        #Nạp nhiệm vụ cho các drone
        self.ui.Load_MS_all.clicked.connect(lambda: asyncio.create_task(self.upload_ms_all()))

        #Khởi động nhiệm vụ cho các drone
        self.ui.mission_all.clicked.connect(lambda: asyncio.create_task(self.mission_all()))
        self.ui.mission_all_2.clicked.connect(lambda: asyncio.create_task(self.mission_all()))

        #Khi nút goto_all được nhấn thì gọi đến hàm goto_all ra lệnh cho các drone đến vị trí tọa độ được chỉ định
        self.ui.goto_all.clicked.connect(lambda: asyncio.create_task(self.goto_all()))

        #Tạm dừng thực hiện nhiệm vụ các drone
        self.ui.pause_all.clicked.connect(lambda: asyncio.create_task(self.pause_all()))
        self.ui.pause_all_2.clicked.connect(lambda: asyncio.create_task(self.pause_all()))


        #################################################################################################################################################
        '''Tạo chuyển động cho các trang'''
        #Xóa thanh tiêu đề cửa sổ 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 

        #Đặt nền chính thành trong suốt
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      
        #Hiệu ứng đổ bóng
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.ui.btn_home.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        #Áp dụng hiệu ứng đổ bóng vào widget trung tâm
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        #Cài đặt biểu tượng cho cửa sổ
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/github.svg"))
        #Đặt tiêu đề cửa sổ
        self.setWindowTitle("MODERN UI")

        #Window Size grip to resize window
        QSizeGrip(self.ui.size_grip)

        #Thu nhỏ cửa sổ
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())

        #Đóng cửa sổ
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())

        #Mở rộng cửa sổ hoặc cho cửa sổ quay lại kích thước ban đầu
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        #Di chuyển cửa sổ khi kéo chuột trên thanh tiêu đề
        def moveWindow(e):
            #Kiểm tra kích thước cửa sổ có đang như mặc định hay không
            if self.isMaximized() == False: #Không phải trang thái ban đầu
                #Chỉ di chuyển cửa sổ khi cửa sổ có kích thước bị thu nhỏ 
                #Chỉ có thể di chuyển cửa sổ khi chuột trái được nhấp
                if e.buttons() == Qt.LeftButton:  
                    #Di chuyển cửa sổ
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        
        #Sự kiện nhấp chuột/Sự kiện di chuyển chuột/sự kiện kéo vào tiêu đề trên cùng để di chuyển cửa sổ
        self.ui.header_frame.mouseMoveEvent = moveWindow

        #Nút chuyển đổi menu bên trái
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())
        self.show()

        #Các nút để truy cập từng trang
        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)) # Khi nhấn btn_home thì gọi đến page_home được tạo bên file giao diện ui_interface
        self.ui.btn_home.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(255, 255, 255);")) # Đổi màu nút
        self.ui.btn_home.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_home.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_home.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_home.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(118, 118, 118);"))

        self.ui.btn_connect.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_connect)) # khi nhấn btn_connect thì gọi đến page_connect
        self.ui.btn_connect.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(255, 255, 255);"))
        self.ui.btn_connect.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_connect.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_connect.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_connect.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(118, 118, 118);"))

        self.ui.btn_map.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_map))   # Khi nhấn btn_map thì gọi đến page_map
        self.ui.btn_map.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(255, 255, 255);"))
        self.ui.btn_map.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_map.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_map.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_map.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(118, 118, 118);"))

        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_algorithm))   # khi nhấn btn_algorithm thì gọi đến page_algorithm
        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(255, 255, 255);"))
        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_algorithm.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(118, 118, 118);"))

        self.ui.btn_parameter.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_parameter))   # Khi nhấn nút btn_parameter thì gọi đến page_parameter
        self.ui.btn_parameter.clicked.connect(lambda: self.ui.btn_parameter.setStyleSheet("background-color: rgb(255, 255, 255);"))
        self.ui.btn_parameter.clicked.connect(lambda: self.ui.btn_home.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_parameter.clicked.connect(lambda: self.ui.btn_connect.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_parameter.clicked.connect(lambda: self.ui.btn_map.setStyleSheet("background-color: rgb(118, 118, 118);"))
        self.ui.btn_parameter.clicked.connect(lambda: self.ui.btn_algorithm.setStyleSheet("background-color: rgb(118, 118, 118);"))
    

    #Menu trượt bên trái
    def slideLeftMenu(self):
        #Nhận chiều rộng menu bên trái hiện tại
        width = self.ui.slide_menu_container.width()

        #Nếu menu có chiều rộng bằng 0 
        if width == 0:
            #Mở rộng menu
            newWidth = 200
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
        #Nếu menu có chiều rộng max
        else:
            # Trả về chiều rộng menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-justify.svg"))

        #Tạo chuyển động cho quá trình chuyển đổi
        self.animation = QPropertyAnimation(self.ui.slide_menu_container, b"maximumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    #Thêm sự kiện cho chuột vào cửa sổ
    def mousePressEvent(self, event):
        #Lấy vị trí hiện tại của chuột
        self.clickPosition = event.globalPos()
        #Chúng ta sẽ sử dụng giá trị này để di chuyển cửa sổ
    #Cập nhật biểu tượng nút phóng to hoặc thu nhỏ trên cửa sổ
    def restore_or_maximize_window(self):
        #Nếu cửa sổ mở max
        if self.isMaximized():
            self.showNormal()
            #Thay đổi icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            #Thay đổi icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/minimize-2.svg"))
    

    ##############################################################################################################################3333
    # Hàm mở code Map
    async def open_map(self):
        command = "python3 map/DG5.py"
        os.system(f"gnome-terminal -- /bin/bash -c '{command}; exec /bin/bash' &")
    
    ##################################################################################################################################
    '''Các hàm update ảnh cho từng drone'''
    #update image1
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
                self.ui.label_35.setPixmap(pixmap1) #Gán hình ảnh vào widget label_35
                self.ui.label_35.setScaledContents(True) #Thay đổi kích cõ hình ảnh theo khung hình label 35
            else:
                print("No image files found in the directory") 

    #Tạo danh sách tập hợp các ảnh có đuôi jpg chứa trong đường dẫn image_directory1
    def get_image_files1(self):
        # Trả về danh sách các tệp hình ảnh trong thư mục
        return [f for f in os.listdir(self.image_directory1) if f.endswith(".jpg")]

    #update image2
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
    
    #update image3
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
    
    #update image4
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
    
    #update image5
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
    
    #update image6
    '''
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
    '''
    #########################################################################################################################################
    '''Các hàm connect từng drone'''
    #Connect drone 1
    async def Connect_1(self):
        global drone_1 
        print("--Connecting to Drone 1")
        self.ui.drone_status_1.appendPlainText("--Connecting to Drone 1")# In ra cửa sổ drone_status
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Connecting to Drone 1")
        await drone_1.connect() # drone1 tiến hành connect
        print("--Drone 1 Connected")
        await drone_1.action.set_maximum_speed(1.0)
        self.ui.drone_status_1.appendPlainText("--Drone 1 Connected")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Drone 1 Connected")
        self.ui.waiting_connect_1.setText("Drone1 connected")# set widget label có tên waiting_connect_1 hiển thị nội dung "Drone1 connected"
        self.ui.waiting_connect_1.setStyleSheet("color: rgb(0,255,0);")# đổi màu chữ của label
        self.number_drone = self.number_drone + 1
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(1)+"\n")
        await asyncio.gather(self.get_alt_1(), self.get_arm_1(), self.get_batt_1(), self.get_mode_1(), self.get_gps_1(),
                             self.print_status_text_1(), self.information_1()) # Sau khi kết nối thành công thì gọi đến các hàm lấy thông tin
        return None
    
    #Connect drone 2
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
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(2)+"\n")
        await asyncio.gather(self.get_alt_2(), self.get_arm_2(), self.get_batt_2(), self.get_mode_2(), self.get_gps_2(),
                             self.print_status_text_2(), self.information_2())
        return None
    
    #Connect drone 3
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
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(3)+"\n")
        await asyncio.gather(self.get_alt_3(), self.get_arm_3(), self.get_batt_3(), self.get_mode_3(), self.get_gps_3(),
                             self.print_status_text_3())
        return None
    
    #Connect drone 4
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
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(4)+"\n")
        await asyncio.gather(self.get_alt_4(), self.get_arm_4(), self.get_batt_4(), self.get_mode_4(), self.get_gps_4(),
                             self.print_status_text_4())
        return None
    
    #Connect drone 5
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
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(5)+"\n")
        await asyncio.gather(self.get_alt_5(), self.get_arm_5(), self.get_batt_5(), self.get_mode_5(), self.get_gps_5(),
                             self.print_status_text_5())
        return None
    
    #Connect drone 6
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
        with open('drone_num.txt', 'w') as f:
                f.write(str(self.number_drone))
        with open('ID_drone.txt', 'a') as f:
                f.write(str(6)+"\n")
        await asyncio.gather(self.get_alt_6(), self.get_arm_6(), self.get_batt_6(), self.get_mode_6(), self.get_gps_6(),
                             self.print_status_text_6())
        return None
    
    #########################################################################################################################################
    '''Các hàm arm từng drone'''
    #arm drone 1
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
    
    #arm drone 2
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
    
    #arm drone 3
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
    
    #arm drone 4
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
    
    #arm drone 5
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
    
    #arm drone 6
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
    '''Các hàm disarm từng drone'''
    #disarm drone 1
    async def Disarm_1(self):
        print("DisArming...")
        await drone_1.action.disarm()
        print("Drone 1 Disarmed.")
        self.ui.arm_or_disarm_drone1.setText("Drone 1 Disarmed")
        self.ui.arm_or_disarm_drone1.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #disarm drone 2
    async def Disarm_2(self):
        print("DisArming...")
        await drone_2.action.disarm()
        print("Drone 2 Disarmed.")
        self.ui.arm_or_disarm_drone2.setText("Drone 2 Disarmed")
        self.ui.arm_or_disarm_drone2.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #disarm drone 3
    async def Disarm_3(self):
        print("DisArming...")
        await drone_3.action.disarm()
        print("Drone 3 Disarmed.")
        self.ui.arm_or_disarm_drone3.setText("Drone 3 Disarmed")
        self.ui.arm_or_disarm_drone3.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #disarm drone 4
    async def Disarm_4(self):
        print("DisArming...")
        await drone_4.action.disarm()
        print("Drone 4 Disarmed.")
        self.ui.arm_or_disarm_drone4.setText("Drone 4 Disarmed")
        self.ui.arm_or_disarm_drone4.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #disarm drone 5
    async def Disarm_5(self):
        print("DisArming...")
        await drone_5.action.disarm()
        print("Drone 5 Disarmed.")
        self.ui.arm_or_disarm_drone5.setText("Drone 5 Disarmed")
        self.ui.arm_or_disarm_drone5.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #disarm drone 6
    async def Disarm_6(self):
        print("DisArming...")
        await drone_6.action.disarm()
        print("Drone 6 Disarmed.")
        self.ui.arm_or_disarm_drone6.setText("Drone 6 Disarmed")
        self.ui.arm_or_disarm_drone6.setStyleSheet("color: rgb(0,255,0);")
        return None
    
    #######################################################################################################################################
    '''Các hàm takeoff từng drone'''
    #takeoff drone 1
    async def Take_off_1(self):
        high_take_off_1 = float(self.ui.edit_high_drone_1.toPlainText()) # gán giá trị độ cao được nhập vào cho biến high_take_off_1
        if high_take_off_1 > 0: # Nếu giá trị được gán >0 thì thực hiện các lệnh bên trong
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
            await drone_1.action.set_takeoff_altitude(high_take_off_1) # set độ cao để takeoff
            await drone_1.action.takeoff()
        else:   
            print("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.drone_status_1.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #takeoff drone 2
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
            self.ui.drone_status_2.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #takeoff drone 3
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
            self.ui.drone_status_3.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #takeoff drone 4
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
            self.ui.drone_status_4.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #takeoff drone 5
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
            self.ui.drone_status_5.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #takeoff drone 6
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
            self.ui.drone_status_6.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("Please enter a valid altitude for takeoff! (valid >0 )")

    #######################################################################################################################################
    '''Các hàm land từng drone'''
    #land drone 1
    async def Land_1(self):
        await drone_1.action.land() # Hạ cánh drone_1
        print("--Landing drone 1...")
        self.ui.drone_status_1.appendPlainText("--Landing drone 1...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 1...")

    #land drone 2
    async def Land_2(self):
        await drone_2.action.land()
        print("--Landing drone 2...")
        self.ui.drone_status_2.appendPlainText("--Landing drone 2...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 2...")

    #land drone 3
    async def Land_3(self):
        await drone_3.action.land()
        print("--Landing drone 3...")
        self.ui.drone_status_3.appendPlainText("--Landing drone 3...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 3...")

    #land drone 4
    async def Land_4(self):
        await drone_4.action.land()
        print("--Landing drone 4...")
        self.ui.drone_status_4.appendPlainText("--Landing drone 4...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 4...")

    #land drone 5
    async def Land_5(self):
        await drone_5.action.land()
        print("--Landing drone 5...")
        self.ui.drone_status_5.appendPlainText("--Landing drone 5...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 5...")

    #land drone 6
    async def Land_6(self):
        await drone_6.action.land()
        print("--Landing drone 6...")
        self.ui.drone_status_6.appendPlainText("--Landing drone 6...")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Landing drone 6...")

    #######################################################################################################################################
    '''Các hàm mission từng drone'''
    #mission drone 1
    async def mission_drone_1(self):
        # Nhập nhiệm vụ từ file QGroundControl
        file_path1 = '/home/ntd/Documents/src/logs/points/points1.plan'
        self.out1 = None  # Initialize out variable
        try:
            self.out1 = await drone_1.mission_raw.import_qgroundcontrol_mission(file_path1)
            print("Mission 1 imported successfully")
            self.ui.file_uav1.appendPlainText("--Mission drone 1")
            self.ui.file_all_uav.appendPlainText("--Mission drone 1")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 1")
        except Exception as e:
            print(f"Failed to import mission 1: {e}")        
        #self.wait_upload_misson = self.wait_upload_misson + 1
        await asyncio.sleep(2)
        #rtl_altitude = 4  # Adjust as necessary
        #await drone_1.action.set_return_to_launch_altitude(rtl_altitude) 
        # Get the input from the UI field
        input_text1 = self.ui.edit_speed_drone_1.toPlainText()

        # Set rtl_speed1 to 2 if the input is empty; otherwise, convert it to float
        if input_text1.strip() == "":
            rtl_speed1 = 2.0
        else:
            rtl_speed1 = float(input_text1)  # Speed in meters per second
        # Print the speed to confirm the value
        print(f"RTL Speed for drone 1: {rtl_speed1} m/s")
        # Set the maximum speed
        await drone_1.action.set_maximum_speed(rtl_speed1)
        # # Set return to launch after mission
        await drone_1.mission.set_return_to_launch_after_mission(True) # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu    
        # Upload the mission and rally points
        await drone_1.mission_raw.upload_mission(self.out1.mission_items)
        print("Mission 1 uploaded")
        try:
            await asyncio.sleep(1)  # Chờ plugin khởi tạo
            await drone_1.action.arm()
            await drone_1.mission.start_mission()
            print("Mission 1 started successfully")
        except Exception as e:
            print(f"Failed to start mission 1 : {e}")  
        #await drone_1.action.arm()
        self.ui.file_uav1.appendPlainText("--Mission drone 1")
        self.ui.file_all_uav.appendPlainText("--Mission drone 1")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 1")
        #await drone_1.mission.start_mission()
        async for mission_progress in drone_1.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_1()
                break

    #mission drone 2
    async def mission_drone_2(self):
        # Nhập nhiệm vụ từ file QGroundControl
        file_path2 = '/home/ntd/Documents/src/logs/points/points2.plan'
        self.out2 = None  # Initialize out variable
        try:
            self.out2 = await drone_2.mission_raw.import_qgroundcontrol_mission(file_path2)
            print("Mission 2 imported successfully")
            self.ui.file_uav2.appendPlainText("--Mission drone 2")
            self.ui.file_all_uav.appendPlainText("--Mission drone 2")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 2")
        except Exception as e:
            print(f"Failed to import mission 2: {e}")        
        #self.wait_upload_misson = self.wait_upload_misson + 1
        await asyncio.sleep(2)
        #rtl_altitude = 4  # Adjust as necessary
        #await drone_2.action.set_return_to_launch_altitude(rtl_altitude)
        input_text2 = self.ui.edit_speed_drone_2.toPlainText()

        # Set rtl_speed2 to 2 if the input is empty; otherwise, convert it to float
        if input_text2.strip() == "":
            rtl_speed2 = 2.0
        else:
            rtl_speed2 = float(input_text2)  # Speed in meters per second
        # Print the speed to confirm the value
        print(f"RTL Speed for drone 2: {rtl_speed2} m/s")
        # Set the maximum speed
        await drone_2.action.set_maximum_speed(rtl_speed2)
        # # Set return to launch after mission
        await drone_2.mission.set_return_to_launch_after_mission(True) # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu    
        # Upload the mission and rally points
        await drone_2.mission_raw.upload_mission(self.out2.mission_items)
        print("Mission 2 uploaded")
        try:
            await asyncio.sleep(4)  # Chờ plugin khởi tạo
            await drone_2.action.arm()
            await drone_2.mission.start_mission()
            print("Mission 2 started successfully")
        except Exception as e:
            print(f"Failed to start mission 2 : {e}")  
        #await drone_1.action.arm()
        self.ui.file_uav2.appendPlainText("--Mission drone 2")
        self.ui.file_all_uav.appendPlainText("--Mission drone 2")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 2")
        #await drone_1.mission.start_mission()
        async for mission_progress in drone_2.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_2()
                break  
    #mission drone 3
    async def mission_drone_3(self):
        # Nhập nhiệm vụ từ file QGroundControl
        file_path3 = '/home/ntd/Documents/src/logs/points/points3.plan'
        self.out3 = None  # Initialize out variable
        try:
            self.out3 = await drone_3.mission_raw.import_qgroundcontrol_mission(file_path3)
            print("Mission 3 imported successfully")
            self.ui.file_uav3.appendPlainText("--Mission drone 3")
            self.ui.file_all_uav.appendPlainText("--Mission drone 3")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 3")
        except Exception as e:
            print(f"Failed to import mission 3: {e}")        
        #self.wait_upload_misson = self.wait_upload_misson + 1
        await asyncio.sleep(2)
        #rtl_altitude = 4  # Adjust as necessary
        #await drone_3.action.set_return_to_launch_altitude(rtl_altitude)
        input_text3 = self.ui.edit_speed_drone_3.toPlainText()

        # Set rtl_speed2 to 2 if the input is empty; otherwise, convert it to float
        if input_text3.strip() == "":
            rtl_speed3 = 2.0
        else:
            rtl_speed3 = float(input_text3)  # Speed in meters per second
        # Print the speed to confirm the value
        print(f"RTL Speed for drone 3: {rtl_speed3} m/s")
        # Set the maximum speed
        await drone_3.action.set_maximum_speed(rtl_speed3)
        # # Set return to launch after mission
        await drone_3.mission.set_return_to_launch_after_mission(True) # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu    
        # Upload the mission and rally points
        await drone_3.mission_raw.upload_mission(self.out3.mission_items)
        print("Mission 3 uploaded")
        try:
            await asyncio.sleep(1)  # Chờ plugin khởi tạo
            await drone_3.action.arm()
            await drone_3.mission.start_mission()
            print("Mission 3 started successfully")
        except Exception as e:
            print(f"Failed to start mission 3: {e}")  
                #await drone_1.action.arm()
        self.ui.file_uav3.appendPlainText("--Mission drone 3")
        self.ui.file_all_uav.appendPlainText("--Mission drone 3")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 3")
        #await drone_1.mission.start_mission()
        async for mission_progress in drone_3.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_3()
                break
    
  #mission drone 4
    async def mission_drone_4(self):
        # Nhập nhiệm vụ từ file QGroundControl
        file_path4 = '/home/ntd/Documents/src/logs/points/points4.plan'
        self.out4 = None  # Initialize out variable
        try:
            self.out4 = await drone_4.mission_raw.import_qgroundcontrol_mission(file_path4)
            print("Mission 4 imported successfully")
            self.ui.file_uav4.appendPlainText("--Mission drone 4")
            self.ui.file_all_uav.appendPlainText("--Mission drone 4")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 4")
        except Exception as e:
            print(f"Failed to import mission 4: {e}")        
        #self.wait_upload_misson = self.wait_upload_misson + 1
        await asyncio.sleep(2)
        #rtl_altitude = 4  # Adjust as necessary
        #await drone_4.action.set_return_to_launch_altitude(rtl_altitude)
        input_text4 = self.ui.edit_speed_drone_4.toPlainText()

        # Set rtl_speed2 to 2 if the input is empty; otherwise, convert it to float
        if input_text4.strip() == "":
            rtl_speed4 = 2.0
        else:
            rtl_speed4 = float(input_text4)  # Speed in meters per second
        # Print the speed to confirm the value
        print(f"RTL Speed for drone 4: {rtl_speed4} m/s")
        # Set the maximum speed
        await drone_4.action.set_maximum_speed(rtl_speed4)
        # # Set return to launch after mission
        await drone_4.mission.set_return_to_launch_after_mission(True) # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu    
        # Upload the mission and rally points
        await drone_4.mission_raw.upload_mission(self.out4.mission_items)
        print("Mission 4 uploaded")
        try:
            await asyncio.sleep(1)  # Chờ plugin khởi tạo
            await drone_4.action.arm()
            await drone_4.mission.start_mission()
            print("Mission 4 started successfully")
        except Exception as e:
            print(f"Failed to start mission 4: {e}")  
        #await drone_1.action.arm()
        self.ui.file_uav4.appendPlainText("--Mission drone 4")
        self.ui.file_all_uav.appendPlainText("--Mission drone 4")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 4")
        #await drone_1.mission.start_mission()
        async for mission_progress in drone_4.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_4()
                break  
    
  #mission drone 5
    async def mission_drone_5(self):
        # Nhập nhiệm vụ từ file QGroundControl
        file_path5 = '/home/ntd/Documents/src/logs/points/points5.plan'
        self.out5 = None  # Initialize out variable
        try:
            self.out5 = await drone_5.mission_raw.import_qgroundcontrol_mission(file_path5)
            print("Mission 5 imported successfully")
            self.ui.file_uav5.appendPlainText("--Mission drone 5")
            self.ui.file_all_uav.appendPlainText("--Mission drone 5")
            self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 5")
        except Exception as e:
            print(f"Failed to import mission 5: {e}")        
        #self.wait_upload_misson = self.wait_upload_misson + 1
        await asyncio.sleep(2)
        #rtl_altitude = 4  # Adjust as necessary
        #await drone_5.action.set_return_to_launch_altitude(rtl_altitude)
        input_text5 = self.ui.edit_speed_drone_5.toPlainText()

        # Set rtl_speed2 to 2 if the input is empty; otherwise, convert it to float
        if input_text5.strip() == "":
            rtl_speed5 = 2.0
        else:
            rtl_speed5 = float(input_text5)  # Speed in meters per second
        # Print the speed to confirm the value
        print(f"RTL Speed for drone 5: {rtl_speed5} m/s")
        # Set the maximum speed
        await drone_5.action.set_maximum_speed(rtl_speed5)
        # # Set return to launch after mission
        await drone_5.mission.set_return_to_launch_after_mission(True) # Sau khi thực hiện nhiệm vụ xong thì quay trở về vị trí ban đầu    
        # Upload the mission and rally points
        await drone_5.mission_raw.upload_mission(self.out5.mission_items)
        print("Mission 5 uploaded")
        try:
            await asyncio.sleep(1)  # Chờ plugin khởi tạo
            await drone_5.action.arm()
            await drone_5.mission.start_mission()
            print("Mission 5 started successfully")
        except Exception as e:
            print(f"Failed to start mission 5: {e}")  
        #await drone_5.action.arm()
        self.ui.file_uav5.appendPlainText("--Mission drone 5")
        self.ui.file_all_uav.appendPlainText("--Mission drone 5")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("--Mission drone 5")
        #await drone_5.mission.start_mission()
        async for mission_progress in drone_5.mission.mission_progress():
            if mission_progress.current == mission_progress.total:
                await self.RTL_5()
                break  
    
    #mission drone 6
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
    '''Các hàm upload nhiệm vụ cho từng drone'''
    '''   #Upload mission drone 1
    async def upload_ms_1(self):
        # Đọc nội dung file .plan
        with open("points1.plan", "r") as f:
            plan_data = json.load(f)
            print("Plan file content:", plan_data)
        
        # Lấy danh sách các điểm từ file .plan
        mission_items_1 = []
        hight1 = float(self.ui.edit_high_drone_1.toPlainText())  # Độ cao từ giao diện

        # Giả sử các điểm tọa độ nằm trong "mission" -> "items"
        for item in plan_data.get("mission", {}).get("items", []):
            lat1 = item["coordinate"][0]       # Lấy latitude
            lon1 = item["coordinate"][1]       # Lấy longitude
            alt1 = item["coordinate"][2]       # Lấy altitude
            mission_item_1 = MissionItem(
                lat1,
                lon1,
                hight1,             # Độ cao
                float('nan'),       # Không đổi các tham số khác
                False,
                float('nan'),
                float('nan'),
                MissionItem.CameraAction.NONE,
                10,
                float('nan'),
                float('nan'),
                float('nan'),
                float('nan'),
                MissionItem.VehicleAction.NONE
            )
            mission_items_1.append(mission_item_1)

        # Tạo và upload nhiệm vụ
        mission_plan_1 = MissionPlan(mission_items_1)
        await drone_1.mission.set_return_to_launch_after_mission(True)
        await drone_1.mission.upload_mission(mission_plan_1)
        print("-- Drone 1 upload mission: Done")
        self.ui.file_uav1.appendPlainText("-- Drone 1 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 1 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 1 upload mission: Done")
        self.wait_upload_misson += 1

    #Upload mission drone 2
    async def upload_ms_2(self):
        with open("points2.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav2.setPlainText(file_content)
        
        mission_items_2 = [] 
        hight2 = float(self.ui.edit_high_drone_2.toPlainText())
        with open("points2.txt", "r") as file:
            for line in file:
                lat2, lon2 = map(float, line.strip().split(', '))
                mission_item_2 = MissionItem(lat2, 
                                         lon2, 
                                         hight2, 
                                         float('nan'), 
                                         False,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         10,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.VehicleAction.NONE)
                mission_items_2.append(mission_item_2)
        mission_plan_2 = MissionPlan(mission_items_2)
        await asyncio.sleep(1)
        await drone_2.mission.set_return_to_launch_after_mission(True)
        await drone_2.mission.upload_mission(mission_plan_2)
        print("-- Drone 2 upload mission: Done")
        self.ui.file_uav2.appendPlainText("-- Drone 2 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 2 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 2 upload mission: Done")
        self.wait_upload_misson = self.wait_upload_misson + 1

    #Upload mission drone 3
    async def upload_ms_3(self):
        with open("points3.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav3.setPlainText(file_content)

        mission_items_3 = [] 
        hight3 = float(self.ui.edit_high_drone_3.toPlainText())
        with open("points3.txt", "r") as file:
            for line in file:
                lat3, lon3 = map(float, line.strip().split(', '))
                mission_item_3 = MissionItem(lat3, 
                                         lon3, 
                                         hight3, 
                                         float('nan'), 
                                         False,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         10,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.VehicleAction.NONE)
                mission_items_3.append(mission_item_3)
        mission_plan_3 = MissionPlan(mission_items_3)
        await asyncio.sleep(2)
        await drone_3.mission.upload_mission(mission_plan_3)
        print("-- Drone 3 upload mission: Done")
        self.ui.file_uav3.appendPlainText("-- Drone 3 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 3 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 3 upload mission: Done")
        self.wait_upload_misson = self.wait_upload_misson + 1
    
    #Upload mission drone 4
    async def upload_ms_4(self):
        with open("points4.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav4.setPlainText(file_content)
            
        mission_items_4 = [] 
        hight4 = float(self.ui.edit_high_drone_4.toPlainText())
        with open("points4.txt", "r") as file:
            for line in file:
                lat4, lon4 = map(float, line.strip().split(', '))
                mission_item_4 = MissionItem(lat4, 
                                         lon4, 
                                         hight4, 
                                         float('nan'), 
                                         False,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         10,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.VehicleAction.NONE)
                mission_items_4.append(mission_item_4)
        mission_plan_4 = MissionPlan(mission_items_4)
        await asyncio.sleep(3)
        await drone_4.mission.upload_mission(mission_plan_4)
        print("-- Drone 4 upload mission: Done")
        self.ui.file_uav4.appendPlainText("-- Drone 4 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 4 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 4 upload mission: Done")
        self.wait_upload_misson = self.wait_upload_misson + 1

    #Upload mission drone 5
    async def upload_ms_5(self):
        with open("points5.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav5.setPlainText(file_content)
            
        mission_items_5 = [] 
        hight5 = float(self.ui.edit_high_drone_5.toPlainText())
        with open("points5.txt", "r") as file:
            for line in file:
                lat5, lon5 = map(float, line.strip().split(', '))
                mission_item_5 = MissionItem(lat5, 
                                         lon5, 
                                         hight5, 
                                         float('nan'), 
                                         False,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         10,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.VehicleAction.NONE)
                mission_items_5.append(mission_item_5)
        mission_plan_5 = MissionPlan(mission_items_5)
        await asyncio.sleep(4)
        await drone_5.mission.upload_mission(mission_plan_5)
        self.ui.file_uav5.appendPlainText("-- Drone 5 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 5 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 5 upload mission: Done")
        self.wait_upload_misson = self.wait_upload_misson + 1

    #Upload mission drone 6
    async def upload_ms_6(self):
        with open("detect/detect.txt", "r") as f:
            file_content = f.read()
            print("File content:", file_content)
            self.ui.file_uav6.setPlainText(file_content)
            
        mission_items_6 = [] 
        hight6 = float(self.ui.edit_high_drone_6.toPlainText())
        folder_path = "detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            for line in file:
                lat6, lon6 = map(float, line.strip().split(', '))
                mission_item_6 = MissionItem(lat6, 
                                         lon6, 
                                         hight6, 
                                         float('nan'), 
                                         True,
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.CameraAction.NONE,
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         float('nan'),
                                         MissionItem.VehicleAction.NONE)
                mission_items_6.append(mission_item_6)
        mission_plan_6 = MissionPlan(mission_items_6)
        await asyncio.sleep(5)
        await drone_6.mission.upload_mission(mission_plan_6)
        self.ui.file_uav6.appendPlainText("-- Drone 6 upload mission: Done")
        self.ui.file_all_uav.appendPlainText("-- Drone 6 upload mission: Done")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("-- Drone 6 upload mission: Done")
        await self.mission_drone_6()'''

    #######################################################################################################################################
    #Go to drone 1
    async def goto_1(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_1.telemetry.position():
            height = position.absolute_altitude_m
            await drone_1.action.goto_location(latitude, longtitude, height, 0)


    
    #Go to drone 2
    async def goto_2(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_2.telemetry.position():
            hight2 = position.absolute_altitude_m
            await drone_2.action.goto_location(latitude, longtitude, hight2, 0)

    #Go to drone 3
    async def goto_3(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_3.telemetry.position():
            hight3 = position.absolute_altitude_m
            await drone_3.action.goto_location(latitude, longtitude, hight3, 0)

    #Go to drone 4
    async def goto_4(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_4.telemetry.position():
            hight4 = position.absolute_altitude_m
            await drone_4.action.goto_location(latitude, longtitude, hight4, 0)

    #Go to drone 5
    async def goto_5(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_5.telemetry.position():
            hight5 = position.absolute_altitude_m
            await drone_5.action.goto_location(latitude, longtitude, hight5, 0)

    #Go to drone 6
    async def goto_6(self):
        latitude = float(self.ui.latitude_algorithm.toPlainText())
        longtitude = float(self.ui.longtitude_algorithm.toPlainText())
        print(latitude)
        print(longtitude)
        async for position in drone_6.telemetry.position():
            hight6 = position.absolute_altitude_m
            await drone_6.action.goto_location(latitude, longtitude, hight6, 0)

    #######################################################################################################################################
    #RTL drone 1
    async def RTL_1(self):
        L1 = float(self.ui.edit_high_drone_1.toPlainText())
        await drone_1.action.set_return_to_launch_altitude(L1)
        await drone_1.action.return_to_launch()

    #RTL drone 2
    async def RTL_2(self):
        L2 = float(self.ui.edit_high_drone_2.toPlainText())
        await drone_2.action.set_return_to_launch_altitude(L2)
        await drone_2.action.return_to_launch()

    #RTL drone 3
    async def RTL_3(self):
        L3 = float(self.ui.edit_high_drone_3.toPlainText())
        await asyncio.sleep(1)
        await drone_3.action.set_return_to_launch_altitude(L3)
        await drone_3.action.return_to_launch()

    #RTL drone 4
    async def RTL_4(self):
        L4 = float(self.ui.edit_high_drone_4.toPlainText())
        await drone_4.action.set_return_to_launch_altitude(L4)
        await drone_4.action.return_to_launch()

    #RTL drone 5
    async def RTL_5(self):
        L5 = float(self.ui.edit_high_drone_5.toPlainText())
        await drone_5.action.set_return_to_launch_altitude(L5)
        await drone_5.action.return_to_launch()

    #RTL drone 6
    async def RTL_6(self):
        L6 = float(self.ui.edit_high_drone_6.toPlainText())
        await drone_6.action.set_return_to_launch_altitude(L6)
        await drone_6.action.return_to_launch()

    #######################################################################################################################################
    #Pause mission drone 1
    async def pause_1(self):
        await drone_1.mission.pause_mission()

    #Pause mission drone 2
    async def pause_2(self):
        await drone_2.mission.pause_mission()

    #Pause mission drone 3
    async def pause_3(self):
        await drone_3.mission.pause_mission()

    #Pause mission drone 4
    async def pause_4(self):
        await drone_4.mission.pause_mission()

    #Pause mission drone 5
    async def pause_5(self):
        await drone_5.mission.pause_mission()

    #Pause mission drone 6
    async def pause_6(self):
        await drone_6.mission.pause_mission()

    #######################################################################################################################################
    #connect 6 drone
    async def connect_6_drone(self):
        await asyncio.gather(self.Connect_1(), self.Connect_2(), self.Connect_3(),
                            self.Connect_4(), self.Connect_5(), self.Connect_6())
    
    #arm 6 drone
    async def arm_6_drone(self):
        await asyncio.gather(self.Arming_1(), self.Arming_2(), self.Arming_3(),
                            self.Arming_4(), self.Arming_5(), self.Arming_6())

    #takeoff 6 drone
    async def take_off_6_drone(self):
        await asyncio.gather(self.Take_off_1(), self.Take_off_2(), self.Take_off_3(),
                            self.Take_off_4(), self.Take_off_5(), self.Take_off_6())

    #Land 6 drone
    async def land_6_drone(self):
        await asyncio.gather(self.Land_1(), self.Land_2(), self.Land_3(),
                            self.Land_4(), self.Land_5(), self.Land_6())

    #Mission 6 drone
    async def mission_all(self):
        await asyncio.gather(self.mission_drone_1(), self.mission_drone_2(), self.mission_drone_3(),
                            self.mission_drone_4(), self.mission_drone_5())

    #Upload mission 6 drone
    async def upload_ms_all(self):
        await asyncio.gather(self.upload_ms_1(), self.upload_ms_2(), self.upload_ms_3(),
                             self.upload_ms_4(), self.upload_ms_5())
    
    #Go to 6 drone
    async def goto_all(self):
        await asyncio.gather(self.goto_1(), self.goto_2(), self.goto_3(), self.goto_4(), self.goto_5(), self.goto_6())
    
    #RTL 6 drone
    async def RTL_ALL(self):
        await asyncio.gather(self.RTL_1(), self.RTL_2(), self.RTL_3(), self.RTL_4(), self.RTL_5(), self.RTL_6())

    #Pause mission 6 drone
    async def pause_all(self):
        await asyncio.gather(self.pause_1(), self.pause_2(), self.pause_3(), self.pause_4(), self.pause_5(), self.pause_6()) 

 #############################################################################################################################################   
    async def detect_object(self):
        await self.test3()
        is_detected = False  # Biến cờ để kiểm soát việc thoát khỏi vòng lặp while
        while not is_detected:  # Lặp cho đến khi phát hiện
            folder_path = "detect"
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.txt'):
                    
                    is_detected = True
                    break  # Thoát khỏi vòng lặp for khi phát hiện được file
            await asyncio.sleep(1)
        self.ui.label_166.setText("found object!!!")# set widget label có tên waiting_connect_1 hiển thị nội dung "Drone1 connected"
        self.ui.label_166.setStyleSheet("color: rgb(0,255,0);")# đổi màu chữ của label
        self.ui.file_all_uav.appendPlainText("found object!!!")
        self.ui.plainTextEdit_all_6_uav.appendPlainText("found object!!!")
        folder_path = "detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split(',' ))
        self.ui.file_all_uav.appendPlainText("object latitude: "+ str(lat_detect))
        self.ui.plainTextEdit_all_6_uav.appendPlainText("object latitude: "+ str(lat_detect))
        self.ui.file_all_uav.appendPlainText("object longitude: "+ str(lon_detect))
        self.ui.plainTextEdit_all_6_uav.appendPlainText("object longitude: "+ str(lon_detect))
        #uav_goto = float(self.ui.uav_goto.toPlainText())
        await asyncio.gather(self.upload_ms_6(), self.pause_1(), self.pause_2(), self.pause_3(), self.pause_4(), self.pause_5())
        #await self.compare_distance(self.folders_to_scan)

    async def test3(self):
        subprocess.Popen(["python3", "test3.py"])

###############################################################################################################################################
    async def control_camera(self):
        subprocess.Popen(["python3","../side menu tutorial (copy)/App_controlCamera/main.py"])
        
################################################################################################################################################
    async def khoang_cach(self, lat1, lon1, lat2, lon2):
        R = 6378000  # bán kính Trái Đất (đơn vị: m)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
      
    async def compare_distance(self, num_uav):
        if num_uav <= 0:
            return
        
        folder_path = "detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split( ', '))

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
        folder_path = "detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()  # Đọc toàn bộ nội dung của file
            lat_detect, lon_detect = map(float, content.strip().split( ', '))
        
        if index < 0 or index >= 5:
            raise ValueError("Invalid drone index")

        drone = [drone_1, drone_2, drone_3, drone_4, drone_5][index]
        async for position in drone.telemetry.position():
            if abs(position.latitude_deg - lat_detect) < 0.0001 and abs(position.longitude_deg - lon_detect) < 0.0001:
                print(f"Drone {index+1} is already at the desired location.")
                self.ui.plainTextEdit_all_6_uav.appendPlainText(f"Drone {index+1} is already at the desired location.")
                self.ui.file_all_uav.appendPlainText(f"Drone {index+1} is already at the desired location.")
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
            self.ui.Alt_Rel_uav1.setText(str(alt_rel)+" m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_uav1.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_uav1.setText(str(latitude))
            self.ui.longitude_uav1.setText(str(longitude))
            with open('gps_data1.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))
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
            with open('gps_data2.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))

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
            with open('gps_data3.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))
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
            with open('gps_data4.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))
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
            with open('gps_data5.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))
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
            with open('gps_data6.txt', 'w') as f:
                f.write(str(latitude) + ', ' + str(longitude))
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
#Hàm lấy thông tin setup
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
#Hàm chỉnh sửa thông tin
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

    ##############################################################################################################################3333
    async def all(self):
        await asyncio.gather(self.upload_ms_all(), self.detect_object(), self.wait_mission())

    async def wait_mission(self):
        while True:
            if self.wait_upload_misson == 5:
                await self.mission_all()
                break
            await asyncio.sleep(2)

    ########################################################################################333
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
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.Monitor_drone_1.geometry().width(),
                                        self.ui.Monitor_drone_1.geometry().height(),
                                        Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
        

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = MainWindow()
    window.show()
    
    with loop:
        sys.exit(loop.run_forever())



