# cSpell:ignore imutils pyqt Pixmap ndarray,
import math

import cv2
import imutils
import numpy as np
import pandas as pd

# Pyqt5
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHeaderView


# @pyqtSlot(np.ndarray, tuple)
def convert_cv2qt(cv_img, size=(640, 360)) -> QPixmap:
    """Convert cv image to qt image to display on gui

    Args:
        cv_img (ndarray): BGR image

    Returns:
        image: RGB image with qt format
    """
    (screen_width, screen_height) = size

    cv_img = imutils.resize(imutils.resize(cv_img, width=screen_width), height=screen_height)

    rgb_image = cv2.cvtColor(
        cv_img,
        cv2.COLOR_BGR2RGB,
    )

    h, w, c = rgb_image.shape
    byte_per_line = c * w

    # print("convert_cv2qt", h, w, c, byte_per_line)
    qt_image = QtGui.QImage(
        rgb_image.data,
        w,
        h,
        byte_per_line,
        QtGui.QImage.Format_RGB888,
    )

    qt_image = qt_image.scaled(*size, aspectRatioMode=Qt.KeepAspectRatio)

    return QPixmap.fromImage(qt_image)


def get_values_from_table(table, headers=[]) -> pd.DataFrame:
    """
    Extract values from a table and return them as a DataFrame.

    Args:
        table (QTableWidget): The table widget to extract values from.

    Returns:
        pd.DataFrame: A DataFrame containing the table values.
    """
    headers = ["id", "connection_address", "streaming_address"]
    df_list = []
    for row in range(table.rowCount()):
        row_data = []
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")
        df_list.append(row_data)
    df = pd.DataFrame(df_list, columns=headers)
    return df


def draw_table(
    table, data=None, connection_allow_indexes=None, streaming_enabled_indexes=None, headers=[]
) -> None:
    """
    Draw tables with UAV data and highlight rows based on indexes.

    Args:
        table (QTableWidget): The table widget to extract values from.
        data (pd.DataFrame, optional): The data to populate the tables. Defaults to None.
        indexes (list, optional): The list of indexes to highlight. Defaults to None.

    Returns:
        None
    """

    for i in range(len(data)):
        for colID, header in enumerate(headers):
            table.setItem(i, colID, QtWidgets.QTableWidgetItem(str(data[header][i])))

        if int(data[headers[0]][i]) in connection_allow_indexes:
            table.item(i, 0).setBackground(QtGui.QColor(144, 238, 144))
            table.item(i, 1).setBackground(QtGui.QColor(144, 238, 144))
        else:
            table.item(i, 0).setBackground(QtGui.QColor(255, 160, 122))
            table.item(i, 1).setBackground(QtGui.QColor(255, 160, 122))

        if int(data[headers[0]][i]) in streaming_enabled_indexes:
            table.item(i, 2).setBackground(QtGui.QColor(144, 238, 144))
        else:
            table.item(i, 2).setBackground(QtGui.QColor(255, 160, 122))

    refine_table(table)


def refine_table(table) -> None:
    """
    Refine the appearance of a table by adjusting column widths.

    Args:
        table (QTableWidget): The table widget to refine.

    Returns:
        None
    """
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)


def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    R = 6378000  # radius of Earth in meters
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


# ! Not used
class QtThread(QThread):  # NOTE: slower than using Thread
    change_image_signal = pyqtSignal(np.ndarray, int)

    def __init__(self, cap, uav_index):
        super().__init__()
        self.isRunning = False
        self.cap = cap
        self.uav_index = uav_index

    def run(self):
        self.isRunning = True
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                # print(frame.shape)
                self.change_image_signal.emit(frame, self.uav_index)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if not self.isRunning:
                break
        self.cap.release()

    def stop(self):
        self.isRunning = False
        # self.quit()
        self.wait()
        # self.terminate()
