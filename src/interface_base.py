#!/usr/bin/env python3
# filepath: workspace/src/interface_base.py
"""
UAV Control Interface Base Module

This module provides the main application window for UAV control and monitoring,
implementing the UI components and their event handlers. It serves as the foundation
for the UAV control interface.
"""

import asyncio
import sys
from typing import Any, Dict, List, Optional, Union

import cv2
import numpy as np
from asyncqt import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from config.interface_config import *
from config.stream_config import *
from config.uav_config import *
from Qt.interface_uav import Ui_MainWindow
from utils.logger import Logger, get_logger
from utils.qt_utils import convert_cv2qt

# UI navigation constants
STACKED_WIDGET_INDEXES = {
    "main page": 0, 
    "map page": 1
}

TAB_WIDGET_INDEXES = {
    "all": 0,
    "uav1": 1,
    "uav2": 2,
    "uav3": 3,
    "uav4": 4,
    "uav5": 5,
    "uav6": 6,
    "settings": 7,
    "overview": 8,
}

# Initialize logger
logger = get_logger(name="UAVInterface", console_level="info")


class Interface(QMainWindow):
    """
    Main UAV control interface window.
    
    This class implements the main window of the UAV control application,
    providing UI components and event handlers for interacting with UAVs.
    """
    
    def __init__(self) -> None:
        """Initialize the interface window and set up UI components."""
        super().__init__()

        # Set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Current view tracking
        self.active_tab_index = 0
        self.active_stack_index = 0

        # Initialize UI component references
        self._initialize_ui_component_lists()
        
        # Set up the interface
        self._init_interface()

    def _initialize_ui_component_lists(self) -> None:
        """
        Initialize lists of UI components for easier access.
        
        This groups related UI elements into lists for more efficient code.
        """
        # UAV-specific UI component lists
        self.uav_tabs = [
            self.ui.actionUAV_1_view,
            self.ui.actionUAV_2_view,
            self.ui.actionUAV_3_view,
            self.ui.actionUAV_4_view,
            self.ui.actionUAV_5_view,
            self.ui.actionUAV_6_view,
        ]

        self.uav_stream_screen_views = [
            self.ui.stream_screen_1,
            self.ui.stream_screen_2,
            self.ui.stream_screen_3,
            self.ui.stream_screen_4,
            self.ui.stream_screen_5,
            self.ui.stream_screen_6,
        ]

        self.uav_general_screen_views = [
            self.ui.general_screen_uav_1,
            self.ui.general_screen_uav_2,
            self.ui.general_screen_uav_3,
            self.ui.general_screen_uav_4,
            self.ui.general_screen_uav_5,
            self.ui.general_screen_uav_6,
        ]

        self.uav_ovv_screen_views = [
            self.ui.ovv_screen_uav_1,
            self.ui.ovv_screen_uav_2,
            self.ui.ovv_screen_uav_3,
            self.ui.ovv_screen_uav_4,
            self.ui.ovv_screen_uav_5,
            self.ui.ovv_screen_uav_6,
        ]

        self.uav_information_views = [
            self.ui.information_uav_1,
            self.ui.information_uav_2,
            self.ui.information_uav_3,
            self.ui.information_uav_4,
            self.ui.information_uav_5,
            self.ui.information_uav_6,
        ]

        self.uav_status_views = [
            self.ui.status_uav_1,
            self.ui.status_uav_2,
            self.ui.status_uav_3,
            self.ui.status_uav_4,
            self.ui.status_uav_5,
            self.ui.status_uav_6,
        ]

        self.uav_update_commands = [
            self.ui.cmdLine_uav_1,
            self.ui.cmdLine_uav_2,
            self.ui.cmdLine_uav_3,
            self.ui.cmdLine_uav_4,
            self.ui.cmdLine_uav_5,
            self.ui.cmdLine_uav_6,
        ]

        self.uav_label_params = [
            self.ui.label_param_uav_1,
            self.ui.label_param_uav_2,
            self.ui.label_param_uav_3,
            self.ui.label_param_uav_4,
            self.ui.label_param_uav_5,
            self.ui.label_param_uav_6,
        ]

        self.uav_param_displays = [
            self.ui.param_current_uav_1,
            self.ui.param_current_uav_2,
            self.ui.param_current_uav_3,
            self.ui.param_current_uav_4,
            self.ui.param_current_uav_5,
            self.ui.param_current_uav_6,
        ]

        self.uav_param_sets = [
            self.ui.param_set_uav_1,
            self.ui.param_set_uav_2,
            self.ui.param_set_uav_3,
            self.ui.param_set_uav_4,
            self.ui.param_set_uav_5,
            self.ui.param_set_uav_6,
        ]

        self.uav_set_param_buttons = [
            self.ui.btn_param_set_uav_1,
            self.ui.btn_param_set_uav_2,
            self.ui.btn_param_set_uav_3,
            self.ui.btn_param_set_uav_4,
            self.ui.btn_param_set_uav_5,
            self.ui.btn_param_set_uav_6,
        ]

        self.uav_get_param_buttons = [
            self.ui.btn_param_dis_uav_1,
            self.ui.btn_param_dis_uav_2,
            self.ui.btn_param_dis_uav_3,
            self.ui.btn_param_dis_uav_4,
            self.ui.btn_param_dis_uav_5,
            self.ui.btn_param_dis_uav_6,
        ]

        self.uav_sett_goTo_buttons = [
            self.ui.btn_sett_goto_uav_all,
            self.ui.btn_sett_goto_uav_1,
            self.ui.btn_sett_goto_uav_2,
            self.ui.btn_sett_goto_uav_3,
            self.ui.btn_sett_goto_uav_4,
            self.ui.btn_sett_goto_uav_5,
            self.ui.btn_sett_goto_uav_6,
        ]

        self.uav_ovv_goTo_buttons = [
            self.ui.btn_ovv_goto_uav_all,
            self.ui.btn_ovv_goto_uav_1,
            self.ui.btn_ovv_goto_uav_2,
            self.ui.btn_ovv_goto_uav_3,
            self.ui.btn_ovv_goto_uav_4,
            self.ui.btn_ovv_goto_uav_5,
            self.ui.btn_ovv_goto_uav_6,
        ]

        self.sett_checkBox_active_lists = [
            self.ui.sett_checkBox_active_uav_1,
            self.ui.sett_checkBox_active_uav_2,
            self.ui.sett_checkBox_active_uav_3,
            self.ui.sett_checkBox_active_uav_4,
            self.ui.sett_checkBox_active_uav_5,
            self.ui.sett_checkBox_active_uav_6,
        ]

        self.sett_checkBox_detect_lists = [
            self.ui.sett_checkBox_detect_uav_1,
            self.ui.sett_checkBox_detect_uav_2,
            self.ui.sett_checkBox_detect_uav_3,
            self.ui.sett_checkBox_detect_uav_4,
            self.ui.sett_checkBox_detect_uav_5,
            self.ui.sett_checkBox_detect_uav_6,
        ]

        self.ovv_checkBox_detect_lists = [
            self.ui.ovv_checkBox_detect_uav_1,
            self.ui.ovv_checkBox_detect_uav_2,
            self.ui.ovv_checkBox_detect_uav_3,
            self.ui.ovv_checkBox_detect_uav_4,
            self.ui.ovv_checkBox_detect_uav_5,
            self.ui.ovv_checkBox_detect_uav_6,
        ]

    def _init_interface(self) -> None:
        """
        Initialize the application interface.
        
        Sets up the UI components with their default values, configures images,
        initializes callbacks, and sets default view states.
        """
        try:
            # Set logos and images
            self._setup_images()
            
            # Set default views
            self.ui.stackedWidget.setCurrentIndex(self.active_stack_index)
            self.ui.tabWidget.setCurrentIndex(self.active_tab_index)
            
            # Set up event handlers
            self._setup_event_handlers()
            
            logger.info("Interface initialization completed successfully")
        except Exception as e:
            logger.error(f"Interface initialization failed: {e}")
            self.popup_msg(
                msg=str(e),
                src_msg="_init_interface",
                type_msg="error"
            )

    def _setup_images(self) -> None:
        """Configure all static images in the interface."""
        # Set up logos
        self._setup_logo_images()
        
        # Set up icon images
        self._setup_icon_images()
        
        # Set default screen images
        self._setup_default_screen_images()

    def _setup_logo_images(self) -> None:
        """Set up the logo images in the interface."""
        # Main logo images
        self.ui.page_name.setPixmap(QtGui.QPixmap(logo1_path))
        self.ui.page_name.setScaledContents(True)
        self.ui.page_name_2.setPixmap(QtGui.QPixmap(logo1_path))
        self.ui.page_name_2.setScaledContents(True)
        
        # Secondary logo images
        self.ui.logo2_2.setPixmap(QtGui.QPixmap(logo2_path))
        self.ui.logo2_2.setScaledContents(True)
        self.ui.logo2.setPixmap(QtGui.QPixmap(logo2_path))
        self.ui.logo2.setScaledContents(True)
        
        # Set application icon
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(app_icon_path)))

    def _setup_icon_images(self) -> None:
        """Set up button icons in the interface."""
        # Set button icons with error handling
        icon_mappings = {
            self.ui.btn_arm: arm_icon_path,
            self.ui.btn_disarm: disarm_icon_path,
            self.ui.btn_open_close: open_close_icon_path,
            self.ui.btn_landing: landing_icon_path,
            self.ui.btn_take_off: takeoff_icon_path,
            self.ui.btn_pause_resume: pause_icon_path,
            self.ui.btn_connect: connect_icon_path,
            self.ui.btn_rtl: rtl_icon_path,
            self.ui.btn_return: return_icon_path,
            self.ui.btn_mission: mission_icon_path,
            self.ui.btn_push_mission: push_mission_icon_path,
            self.ui.btn_toggle_camera: toggle_icon_path
        }
        
        for button, icon_path in icon_mappings.items():
            try:
                button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))
            except Exception as e:
                logger.warning(f"Failed to set icon for button: {e}")

    def _setup_default_screen_images(self) -> None:
        """Set default 'no signal' images for all screen views."""
        # Set default images for general screens
        for screen in self.uav_general_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["general_screen"]))
            screen.setScaledContents(False)
            
        # Set default images for stream screens
        for screen in self.uav_stream_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["stream_screen"]))
            screen.setScaledContents(False)
            
        # Set default images for overview screens
        for screen in self.uav_ovv_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["ovv_screen"]))
            screen.setScaledContents(False)

    def _setup_event_handlers(self) -> None:
        """Set up all event handlers for the interface."""
        # Set up menu bar event handlers
        self._setup_menu_bar_events()
        
        # Set up tab clicked events
        self._setup_tab_events()

    def _setup_menu_bar_events(self) -> None:
        """Set up menu bar action event handlers."""
        try:
            # UAV view actions
            self.ui.actionUAV_1_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav1")
            )
            self.ui.actionUAV_2_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav2")
            )
            self.ui.actionUAV_3_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav3")
            )
            self.ui.actionUAV_4_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav4")
            )
            self.ui.actionUAV_5_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav5")
            )
            self.ui.actionUAV_6_view.triggered.connect(
                lambda: self._switch_layout("main page", "uav6")
            )
            
            # Overview and settings actions
            self.ui.actionOverview.triggered.connect(
                lambda: self._switch_layout("main page", "all")
            )
            self.ui.actionScreen_10_Settings.triggered.connect(
                lambda: self._switch_layout("main page", "settings")
            )
            self.ui.actionScreen_7_Rescue_map.triggered.connect(
                lambda: self._switch_layout("map page", "all")
            )
            self.ui.actionScreen_11_Overview.triggered.connect(
                lambda: self._switch_layout("main page", "overview")
            )
        except Exception as e:
            logger.error(f"Error setting up menu bar events: {e}")
            self.popup_msg(str(e), src_msg="_setup_menu_bar_events", type_msg="error")

    def _setup_tab_events(self) -> None:
        """Set up tab bar clicked event handler."""
        try:
            self.ui.tabWidget.tabBarClicked.connect(self._switch_tab)
        except Exception as e:
            logger.error(f"Error setting up tab events: {e}")
            self.popup_msg(str(e), src_msg="_setup_tab_events", type_msg="error")

    def _switch_tab(self, index: int) -> None:
        """
        Switch the active tab to the specified index.
        
        Args:
            index: The index of the tab to switch to
        """
        self.active_tab_index = index
        self.active_stack_index = self.ui.stackedWidget.currentIndex()
        logger.debug(f"Switched to tab index {index}")

    def _switch_layout(self, stack_name: str, tab_name: str) -> None:
        """
        Switch the layout to the specified stack and tab.
        
        Args:
            stack_name: Name of the stack to switch to
            tab_name: Name of the tab to switch to
        """
        try:
            # Validate inputs
            if stack_name not in STACKED_WIDGET_INDEXES:
                raise ValueError(f"Invalid stack name: {stack_name}")
            if tab_name not in TAB_WIDGET_INDEXES:
                raise ValueError(f"Invalid tab name: {tab_name}")
                
            # Switch views
            self.ui.stackedWidget.setCurrentIndex(STACKED_WIDGET_INDEXES[stack_name])
            self.ui.tabWidget.setCurrentIndex(TAB_WIDGET_INDEXES[tab_name])
            
            # Update tracking variables
            self.active_tab_index = self.ui.tabWidget.currentIndex()
            self.active_stack_index = self.ui.stackedWidget.currentIndex()
            
            logger.debug(f"Switched layout to {stack_name}, {tab_name}")
        except Exception as e:
            logger.error(f"Failed to switch layout: {e}")
            self.popup_msg(str(e), src_msg="_switch_layout", type_msg="error")

    # ----------------------------- UI Display Utility Functions -----------------------------

    def template_information(
        self,
        uav_index: int,
        connection_status: str = "No information",
        arming_status: str = "No information",
        battery_status: str = "No information",
        gps_status: str = "No information",
        mode_status: str = "No information",
        actuator_status: str = "No information",
        altitude_status: List[str] = None,
        position_status: List[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a formatted information display template for a UAV.
        
        Args:
            uav_index: Index of the UAV
            connection_status: Connection status string
            arming_status: Arming status string
            battery_status: Battery status string
            gps_status: GPS status string
            mode_status: Flight mode status string
            actuator_status: Actuator status string
            altitude_status: List of [relative_altitude, MSL_altitude]
            position_status: List of [latitude, longitude]
            **kwargs: Additional parameters for future expansion
            
        Returns:
            Formatted string containing UAV information
        """
        # Default values for list parameters
        if altitude_status is None:
            altitude_status = ["No information", "No information"]
        if position_status is None:
            position_status = ["No information", "No information"]
            
        # Format the information string
        _translate = QtCore.QCoreApplication.translate
        msg = "\n".join([
            f"\t**UAV {uav_index} Information**:".strip(),
            f"{'- Connection:' : <20}{str(connection_status) : ^10}".strip(),
            f"{'- Arming:': <20}{arming_status : ^10}".strip(),
            f"{'- Battery:': <20}{battery_status : ^10}".strip(),
            f"{'- GPS(FIXED):': <20}{gps_status: ^10}".strip(),
            f"{'- Mode:': <20}{mode_status : ^10}".strip(),
            f"{'- Actuator:': <20}{actuator_status : ^10}".strip(),
            f"{'- Altitude:': <20}".strip(),
            f"{'-----Rel:': <20}{altitude_status[0] : ^16}m".strip(),
            f"{'-----MSL:': <20}{altitude_status[1] : ^16}m".strip(),
            f"{'- Position:': <20}".strip(),
            f"{'-----Latitude:': <20}{position_status[0] : ^16}".strip(),
            f"{'-----Longitude:': <20}{position_status[1] : ^16}".strip(),
            "================================",
        ])
        
        return _translate("MainWindow", msg)

    def update_terminal(self, text: str, uav_index: int = 0) -> None:
        """
        Update the specified terminal with text.
        
        Args:
            text: Text to append to the terminal
            uav_index: Index of the UAV terminal to update (0 for main terminal)
        """
        try:
            if uav_index == 0:
                # Update main terminal
                self.ui.mainTerminal.setFocus()
                self.ui.mainTerminal.moveCursor(self.ui.mainTerminal.textCursor().End)
                self.ui.mainTerminal.appendPlainText(text)
            elif 1 <= uav_index <= MAX_UAV_COUNT:
                # Update UAV-specific terminal
                terminal = self.uav_status_views[uav_index - 1]
                terminal.setFocus()
                terminal.moveCursor(terminal.textCursor().End)
                terminal.appendPlainText(text)
            else:
                logger.warning(f"Invalid UAV index for terminal update: {uav_index}")
        except Exception as e:
            logger.error(f"Failed to update terminal: {e}")

    def update_uav_screen_view(
        self, 
        uav_index: int, 
        frame: Optional[np.ndarray] = None, 
        screen_name: str = "all"
    ) -> None:
        """
        Update the screen view for a UAV with the specified frame.
        
        Args:
            uav_index: Index of the UAV (1-based)
            frame: Video frame to display (None for pause image)
            screen_name: Name of the screen to update ("general_screen", 
                        "stream_screen", "ovv_screen", or "all")
        """
        try:
            # Validate UAV index
            if not 1 <= uav_index <= MAX_UAV_COUNT:
                logger.warning(f"Invalid UAV index: {uav_index}")
                return
                
            # Map of screen names to UI components
            screen_views = {
                "general_screen": self.uav_general_screen_views[uav_index - 1],
                "stream_screen": self.uav_stream_screen_views[uav_index - 1],
                "ovv_screen": self.uav_ovv_screen_views[uav_index - 1],
            }
            
            if screen_name != "all":
                # Update a specific screen
                if screen_name not in screen_views:
                    logger.warning(f"Invalid screen name: {screen_name}")
                    return
                    
                # Use pause image if no frame is provided
                if frame is None:
                    frame = cv2.imread(pause_img_paths[screen_name])
                
                # Convert and display frame
                width, height = screen_sizes[screen_name]
                pixmap = convert_cv2qt(frame, size=(width, height))
                screen_views[screen_name].setPixmap(pixmap)
            else:
                # Update all screens
                for name in ["general_screen", "ovv_screen", "stream_screen"]:
                    self.update_uav_screen_view(uav_index, frame, screen_name=name)
                    
        except Exception as e:
            logger.error(f"Failed to update UAV screen view: {e}")

    def popup_msg(self, msg: str, src_msg: str = "", type_msg: str = "error") -> None:
        """
        Display a popup message dialog.
        
        Args:
            msg: Message to display
            src_msg: Source context of the message
            type_msg: Message type ('warning', 'error', or 'info')
        """
        try:
            # Log the message
            logger.log(f"From: {src_msg}\n[!] Details: {msg}", level=type_msg.lower())
            
            # Create and configure message box
            popup = QMessageBox(self)
            
            # Set icon based on message type
            if type_msg.lower() == "warning":
                popup.setIcon(QMessageBox.Warning)
            elif type_msg.lower() == "error":
                popup.setIcon(QMessageBox.Critical)
            elif type_msg.lower() == "info":
                popup.setIcon(QMessageBox.Information)
            else:
                popup.setIcon(QMessageBox.Information)
                
            # Set message and show dialog
            popup.setText(f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            
        except Exception as e:
            # Fallback for errors in the popup system itself
            print(f"Error displaying popup: {e}")
            print(f"Original message: {msg}")


def run() -> None:
    """
    Run the main application.
    
    Initializes the Qt application with asyncio integration and shows the main window.
    """
    try:
        # Create Qt application
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle("Oxygen")  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
        
        # Set up asyncio integration
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        # Create and show main window
        main_window = Interface()
        main_window.show()
        
        # Run event loop
        with loop:
            # Cancel any pending tasks
            pending = asyncio.all_tasks(loop=loop)
            for task in pending:
                task.cancel()
                
            # Exit with the event loop's result
            sys.exit(loop.run_forever())
            
    except Exception as e:
        logger.critical(f"Application startup failed: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()