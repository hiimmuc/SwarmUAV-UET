#!/usr/bin/env python3
# filepath: /media/phgnam-d/920C22060C21E5C7/Personal/Workspace/UAV/workspace/src/utils/qt_utils.py
"""
PyQt Utilities

This module provides utility functions for working with PyQt widgets, particularly
for handling image conversion, table management, and system information.
"""

import platform
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import pandas as pd
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

# Define color constants for better readability and consistency
COLOR_GREEN = QColor(144, 238, 144)  # Light green
COLOR_RED = QColor(255, 160, 122)    # Light red/salmon


def convert_cv2qt(cv_img: np.ndarray, size: Tuple[int, int] = (640, 360)) -> QPixmap:
    """
    Convert OpenCV image to PyQt QPixmap for display in GUI.
    
    Args:
        cv_img: OpenCV image in BGR format
        size: Target image size as (width, height)
        
    Returns:
        QPixmap object ready for display in Qt widgets
        
    Note:
        This function handles resizing, color space conversion, and proper
        aspect ratio maintenance.
    """
    # Validate input
    if cv_img is None or cv_img.size == 0:
        # Return an empty pixmap if the input is invalid
        return QPixmap(*size)

    # Resize image while preserving aspect ratio
    rgb_image = cv2.cvtColor(
        src=cv2.resize(src=cv_img, dsize=size, interpolation=cv2.INTER_AREA),
        code=cv2.COLOR_BGR2RGB,
    )

    # Create QImage from numpy array
    h, w, c = rgb_image.shape
    byte_per_line = c * w
    qt_image = QtGui.QImage(
        rgb_image.data,
        w,
        h,
        byte_per_line,
        QtGui.QImage.Format_RGB888,
    )

    # Scale with proper aspect ratio
    qt_image = qt_image.scaled(*size, aspectRatioMode=Qt.KeepAspectRatio)

    # Convert to QPixmap
    return QPixmap.fromImage(qt_image)


def get_values_from_table(
    table_widget: QTableWidget, headers: List[str] = None
) -> pd.DataFrame:
    """
    Extract values from a QTableWidget and return them as a DataFrame.
    
    Args:
        table_widget: The table widget to extract values from
        headers: Column headers for the DataFrame (optional)
        
    Returns:
        DataFrame containing the table values
        
    Note:
        If headers are not provided, default UAV-related headers will be used.
    """
    # Default headers if none provided
    if headers is None or not headers:
        headers = ["id", "connection_address", "streaming_address"]
    
    # Extract data from table_widget
    data = []
    for row in range(table_widget.rowCount()):
        row_data = []
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")
        data.append(row_data)
    
    # Create DataFrame with appropriate headers
    return pd.DataFrame(data, columns=headers[:table_widget.columnCount()])


def draw_table(
    table_widget: QTableWidget, 
    data: pd.DataFrame = None, 
    connection_allow_indexes: List[int] = None, 
    streaming_enabled_indexes: List[int] = None, 
    headers: List[str] = None
) -> None:
    """
    Draw and format a table with UAV data, highlighting rows based on status.
    
    Args:
        table_widget: The table widget to populate
        data: DataFrame containing the data to display
        connection_allow_indexes: List of IDs with allowed connections (highlighted green)
        streaming_enabled_indexes: List of IDs with enabled streaming (highlighted green)
        headers: Column headers to use from the DataFrame
        
    Returns:
        None
        
    Note:
        This function populates the table and applies color coding based on
        connection and streaming status.
    """
    # Handle default parameters
    if data is None:
        return
    
    if connection_allow_indexes is None:
        connection_allow_indexes = []
        
    if streaming_enabled_indexes is None:
        streaming_enabled_indexes = []
        
    if headers is None or not headers:
        headers = list(data.columns)
    
    # Ensure table has enough rows
    row_count = len(data)
    if table_widget.rowCount() < row_count:
        table_widget.setRowCount(row_count)
    
    # Populate table with data
    for i in range(row_count):
        for col_id, header in enumerate(headers):
            if col_id < table_widget.columnCount() and header in data.columns:
                value = str(data[header].iloc[i])
                item = QTableWidgetItem(value)
                table_widget.setItem(i, col_id, item)
        
        # Apply color coding based on status
        if 'id' in data.columns:
            row_id = int(data['id'].iloc[i])
            
            # Highlight connection status (columns 0 and 1)
            connection_color = COLOR_GREEN if row_id in connection_allow_indexes else COLOR_RED
            for col in range(min(2, table_widget.columnCount())):
                if table_widget.item(i, col):
                    table_widget.item(i, col).setBackground(connection_color)
            
            # Highlight streaming status (column 2)
            if table_widget.columnCount() > 2 and table_widget.item(i, 2):
                streaming_color = COLOR_GREEN if row_id in streaming_enabled_indexes else COLOR_RED
                table_widget.item(i, 2).setBackground(streaming_color)
    
    # Apply table formatting
    refine_table(table_widget)


def refine_table(table_widget: QTableWidget) -> None:
    """
    Refine the appearance of a table_widget by adjusting column widths and styling.
    
    Args:
        table_widget: The table widget to refine
        
    Returns:
        None
        
    Note:
        This sets the first column to fit content width and stretches other columns.
    """
    if table_widget is None:
        return
        
    # Get table_widget header
    header = table_widget.horizontalHeader()
    if header is None:
        return
    
    # Set column resize modes
    column_count = table_widget.columnCount()
    
    if column_count > 0:
        # First column (ID) should resize to contents
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        # Other columns should stretch to fill available space
        for i in range(1, column_count):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
    
    # Additional styling (optional)
    table_widget.setAlternatingRowColors(True)
    table_widget.setShowGrid(True)
    table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


def get_system_information() -> str:
    """
    Get formatted system information as a string.
    
    Returns:
        Formatted string containing system information
        
    Note:
        This includes OS, architecture, hostname, and processor details.
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
    
    # Format as string with line breaks
    return "\n".join(f"{key}: {value}" for key, value in system_info.items())


def create_status_indicator(status: bool = False, size: int = 15) -> QtWidgets.QLabel:
    """
    Create a colored status indicator label.
    
    Args:
        status: True for active/on status (green), False for inactive/off (red)
        size: Size of the indicator in pixels
        
    Returns:
        QLabel configured as a colored status indicator
    """
    indicator = QtWidgets.QLabel()
    indicator.setFixedSize(size, size)
    indicator.setStyleSheet(
        f"background-color: {'green' if status else 'red'}; "
        f"border-radius: {size//2}px; "
        f"margin: 2px;"
    )
    indicator.setToolTip("Active" if status else "Inactive")
    return indicator


def set_widget_stylesheet(widget: QtWidgets.QWidget, style_type: str = "default") -> None:
    """
    Apply a predefined stylesheet to a widget.
    
    Args:
        widget: The widget to style
        style_type: Type of style to apply ('default', 'dark', 'light', etc.)
        
    Returns:
        None
    """
    styles = {
        "default": """
            QWidget {
                font-family: Arial;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QTableWidget {
                alternate-background-color: #f5f5f5;
                gridline-color: #d0d0d0;
            }
        """,
        "dark": """
            QWidget {
                background-color: #2d2d2d;
                color: #f0f0f0;
                font-family: Arial;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #3d3d3d;
                border: 1px solid #5d5d5d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
            QTableWidget {
                alternate-background-color: #3d3d3d;
                gridline-color: #5d5d5d;
                color: #f0f0f0;
            }
        """
    }
    
    if style_type in styles:
        widget.setStyleSheet(styles[style_type])


# Example usage
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    # Create a simple demo window
    window = QtWidgets.QWidget()
    window.setWindowTitle("PyQt Utilities Demo")
    window.resize(800, 600)
    
    # Create layout
    layout = QtWidgets.QVBoxLayout(window)
    
    # System info
    info_label = QtWidgets.QLabel(get_system_information())
    layout.addWidget(info_label)
    
    # Table demo
    table = QtWidgets.QTableWidget(5, 3)
    table.setHorizontalHeaderLabels(["ID", "Connection", "Streaming"])
    
    # Sample data
    data = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "connection_address": ["udp://127.0.0.1:14540", "udp://127.0.0.1:14541", 
                             "udp://127.0.0.1:14542", "udp://127.0.0.1:14543", 
                             "udp://127.0.0.1:14544"],
        "streaming_address": ["rtsp://127.0.0.1:8554/1", "rtsp://127.0.0.1:8554/2",
                            "rtsp://127.0.0.1:8554/3", "rtsp://127.0.0.1:8554/4",
                            "rtsp://127.0.0.1:8554/5"]
    })
    
    # Draw table with sample data
    draw_table(
        table, 
        data=data, 
        connection_allow_indexes=[1, 3, 5], 
        streaming_enabled_indexes=[1, 2]
    )
    
    layout.addWidget(table)
    
    # Status indicators
    status_layout = QtWidgets.QHBoxLayout()
    status_layout.addWidget(QtWidgets.QLabel("Connection Status:"))
    status_layout.addWidget(create_status_indicator(True))
    status_layout.addWidget(QtWidgets.QLabel("Streaming Status:"))
    status_layout.addWidget(create_status_indicator(False))
    status_layout.addStretch()
    
    layout.addLayout(status_layout)
    
    # Apply stylesheet
    set_widget_stylesheet(window, "default")
    
    # Show window
    window.show()
    sys.exit(app.exec_())