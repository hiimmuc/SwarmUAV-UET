# cSpell:ignore imutils pyqt Pixmap ndarray,

import platform

import cv2
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

    rgb_image = cv2.cvtColor(
        src=cv2.resize(src=cv_img, dsize=size, interpolation=cv2.INTER_NEAREST),
        code=cv2.COLOR_BGR2RGB,
    )

    h, w, c = rgb_image.shape
    byte_per_line = c * w

    qt_image = QtGui.QImage(
        rgb_image.data,
        w,
        h,
        byte_per_line,
        QtGui.QImage.Format_RGB888,
    )

    qt_image = qt_image.scaled(*size, aspectRatioMode=Qt.KeepAspectRatio)

    return QPixmap(
        QPixmap.fromImage(
            qt_image,
        )
    )


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


def get_system_information():
    """
    Get system information

    Returns:
        dict: System information
    """
    system_info = {
        "System": platform.system(),
        "Architecture": platform.architecture(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }
    information = ""
    for key, value in system_info.items():
        information += f"{key}: {value}\n"
    return information
