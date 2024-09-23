import math
import os
import sys
from pathlib import Path

import cv2
import imutils
import numpy as np
import pandas as pd

# Pyqt5
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHeaderView


def convert_cv2qt(cv_img, size=(640, 360)) -> QPixmap:
    """Convert cv image to qt image to display on gui

    Args:
        cv_img (ndarray): BGR image

    Returns:
        image: RGB image with qt format
    """

    rgb_image = cv2.cvtColor(cv2.resize(cv_img, size), cv2.COLOR_BGR2RGB)

    qt_image = QtGui.QImage(
        rgb_image,
        rgb_image.shape[1],
        rgb_image.shape[0],
        rgb_image.strides[0],
        QtGui.QImage.Format_RGB888,
    )
    # p = convert_to_Qt_format.scaled(*size, Qt.KeepAspectRatio)
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


def draw_table(table, data=None, indexes=None, headers=[]) -> None:
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

        if int(data[headers[0]][i]) in indexes:
            set_row_color(table, i, QtGui.QColor(144, 238, 144))
        else:
            set_row_color(table, i, QtGui.QColor(255, 160, 122))

    refine_table(table)


def set_row_color(table, row, color) -> None:
    for col in range(table.columnCount()):
        table.item(row, col).setBackground(color)


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
    R = 6378000  # bán kính Trái Đất (đơn vị: m)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
