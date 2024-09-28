import asyncio
import os
import sys
from pathlib import Path
from threading import Thread

# import acapture
import cv2
import numpy as np
from asyncqt import QEventLoop, asyncSlot
from imutils.video import FPS

#
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

# Pyqt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QWidget

#
from map_utils import *
from UI.interface_uav import *
from utils import *

parent_dir = Path(__file__).parent

MAX_UAV_COUNT = 6

PROTO = "udp"
SERVER_HOST = ""
DEFAULT_PORT = 50060
DEFAULT_BIND_PORT = 14541

FPS = 33

screen_sizes = {
    "general_screen": (333, 592),
    "stream_screen": (720, 1280),
    "ovv_screen": (180, 320),
}

stackedWidget_indexes = {"main page": 0, "map page": 1}

tabWidget_indexes = {
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

UAVs = {
    1: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 0),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 0}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{1}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
    2: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 1),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 1}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{2}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
    3: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 2),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 2}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{3}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
    4: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 3),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 3}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{4}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
    5: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 4),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 4}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{5}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
    6: {
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + 5),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + 5}",
        "streaming_address": f"{parent_dir.parent}/assets/videos/cam{6}.mp4",
        "connection_allow": True,
        "streaming_enable": True,
    },
}


class App(QMainWindow):
    """
    A class to represent the main application window for UAV control.
    """

    def __init__(self, model=None) -> None:
        QMainWindow.__init__(self)
        # QWidget.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # starting stack and tab index
        self.active_tab_index = 0
        self.active_stack_index = 0

        # UAVs
        self.uav_stream_threads = [None for _ in range(1, MAX_UAV_COUNT + 1)]

        self.uav_stream_captures = [None for _ in range(1, MAX_UAV_COUNT + 1)]

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

        #
        self.init_application()
        # ---------------------------------------------------------

    def init_application(self) -> None:
        """
        Initializes the application by setting up the UI components and their default values.

        This method performs the following tasks:
        - Resets the paths for assets and videos.
        - Sets the pixmaps and scaled contents for various UI elements such as logos and screen views.
        - Sets the URL for map views.
        - Sets default values for checkboxes and other UI elements.
        - Sets the default tab and stack index.
        - Initializes various map-related callbacks and events.
        - Draws tables with default data and indexes.
        - Initializes the map engine and sets up map and marker event callbacks.

        Returns:
            None
        """
        # reset path for assets and videos
        basePath = Path(__file__)
        basePath = basePath.resolve().parents[0].parents[0]

        # set logo
        self.ui.page_name.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logo1.png"))
        self.ui.page_name.setScaledContents(True)
        self.ui.page_name_2.setPixmap(
            QtGui.QPixmap(f"{basePath}/assets/icons/logo1.png")
        )
        self.ui.page_name_2.setScaledContents(True)
        self.ui.logo2_2.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logoUET.png"))
        self.ui.logo2_2.setScaledContents(True)
        self.ui.logo2.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logoUET.png"))
        self.ui.logo2.setScaledContents(True)

        # screen view default image
        for screen in self.uav_general_screen_views:
            screen.setPixmap(QtGui.QPixmap(f"{basePath}/assets/pictures/nosignal.jpg"))
            screen.setScaledContents(True)
        for screen in self.uav_stream_screen_views:
            screen.setPixmap(
                QtGui.QPixmap(f"{basePath}/assets/pictures/no_signal2.jpg")
            )
            screen.setScaledContents(True)
        for screen in self.uav_ovv_screen_views:
            screen.setPixmap(QtGui.QPixmap(f"{basePath}/assets/pictures/nosignal.jpg"))
            screen.setScaledContents(True)

        # map URL
        self.ui.MapWebView.setUrl(QtCore.QUrl(f"file://{basePath}/assets/map.html"))

        self.ui.Overview_map_view.setUrl(
            QtCore.QUrl(f"file://{basePath}/assets/map.html")
        )

        # set default value for nSwarms
        self.ui.nSwarms_sett.setValue(6)
        self.ui.nSwarms_ovv.setValue(6)

        # set default tab and stack index
        self.ui.stackedWidget.setCurrentIndex(self.active_stack_index)
        self.ui.tabWidget.setCurrentIndex(self.active_tab_index)

        # map events
        self._menu_bar_clicked_event()

        self._tab_clicked_event()

        self._button_clicked_event()

        self._line_edit_event()

        self._uav_to_widgets()

        # set emit signal
        self._create_streaming_threads()

        # init tables
        self._modify_tables(mode="init")
        # init checkboxes
        self._handling_checkBoxes(mode="init")

        # init map
        self.map = MapEngine(self.ui.MapWebView)

        self.map.mapMovedCallback = self.onMapMoved
        self.map.mapClickedCallback = self.onMapLClick
        self.map.mapDoubleClickedCallback = self.onMapDClick
        self.map.mapRightClickedCallback = self.onMapRClick

        self.map.markerMovedCallback = self.onMarkerMoved
        self.map.markerClickedCallback = self.onMarkerLClick
        self.map.markerDoubleClickedCallback = self.onMarkerDClick
        self.map.markerRightClickedCallback = self.onMarkerRClick

        # self.map.polygonDrawnCallback = self.onPolygonDrawn

    # //-/////////////////////////////////////////////////////////////
    # //-/////////////////////////////////////////////////////////////
    # ? map functions to UI
    def _uav_to_widgets(self) -> None:
        """
        Maps UAV components to their respective UI elements.

        This method iterates over a predefined number of UAVs (MAX_UAV_COUNT) and assigns various UI elements
        and initial status information to each UAV. The mapping includes tabs, general screens, overview screens,
        stream screens, information views, update commands, parameter displays, parameter sets, label parameters,
        and current information such as initial height, connection status, arming status, battery status, GPS status,
        mode status, actuator status, altitude status, and position status.

        Attributes:
            UAVs (dict): A dictionary where each key is an index representing a UAV, and the value is another
                            dictionary containing the UI elements and status information for that UAV.
            self.uav_tabs (list): List of tab UI elements for each UAV.
            self.uav_general_screen_views (list): List of general screen UI elements for each UAV.
            self.uav_ovv_screen_views (list): List of overview screen UI elements for each UAV.
            self.uav_stream_screen_views (list): List of stream screen UI elements for each UAV.
            self.uav_information_views (list): List of information view UI elements for each UAV.
            self.uav_update_commands (list): List of update command UI elements for each UAV.
            self.uav_param_displays (list): List of parameter display UI elements for each UAV.
            self.uav_param_sets (list): List of parameter set UI elements for each UAV.
            self.uav_label_params (list): List of label parameter UI elements for each UAV.
        """
        global UAVs
        for i in range(MAX_UAV_COUNT):
            index = i + 1
            UAVs[index]["tab"] = self.uav_tabs[i]
            UAVs[index]["general_screen"] = self.uav_general_screen_views[i]
            UAVs[index]["ovv_screen"] = self.uav_ovv_screen_views[i]
            UAVs[index]["stream_screen"] = self.uav_stream_screen_views[i]
            UAVs[index]["information_view"] = self.uav_information_views[i]
            UAVs[index]["update_command"] = self.uav_update_commands[i]
            UAVs[index]["param_display"] = self.uav_param_displays[i]
            UAVs[index]["param_set"] = self.uav_param_sets[i]
            UAVs[index]["label_param"] = self.uav_label_params[i]
            UAVs[index]["uav_information"] = {
                "init_height": float(5 + i),
                "init_longitude": 8.545594,
                "init_latitude": 47.397823,
                "connection_status": False,
                "streaming_status": False,
                "arming_status": "No information",
                "battery_status": "No information",
                "gps_status": "No information",
                "mode_status": "No information",
                "actuator_status": "No information",
                "altitude_status": ["No information", "No information"],
                "position_status": ["No information", "No information"],
            }

    def _menu_bar_clicked_event(self) -> None:
        """
        Sets up the menu bar actions for various UAV views and other screens.

        This method connects the triggered signals of the menu bar actions to the
        corresponding slots that handle the switching of views. The following actions
        are set up:

        - UAV_1_view: Switches to the main page with UAV 1 view.
        - UAV_2_view: Switches to the main page with UAV 2 view.
        - UAV_3_view: Switches to the main page with UAV 3 view.
        - UAV_4_view: Switches to the main page with UAV 4 view.
        - UAV_5_view: Switches to the main page with UAV 5 view.
        - UAV_6_view: Switches to the main page with UAV 6 view.
        - Overview: Switches to the main page with an overview of all UAVs.
        - Screen_10_Settings: Switches to the main page with settings view.
        - Screen_7_Rescue_map: Switches to the map page with an overview of all UAVs.
        - Screen_11_Overview: Switches to the main page with an overview view.
        """
        # setup tabs menubar actions
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

    def _tab_clicked_event(self) -> None:
        """
        Switches the current view in the UI to the specified stack and tab.

        Args:
            stack_name (str): The name of the stack to switch to.
            tab_name (str): The name of the tab to switch to.

        Returns:
            None
        """
        self.ui.tabWidget.tabBarClicked.connect(self._switch_tab)

    def _button_clicked_event(self) -> None:
        """
        Maps UI button click events to corresponding UAV functions.

        This method connects various UI buttons to their respective UAV control functions
        using asynchronous tasks. The buttons are mapped to functions that handle UAV
        operations such as arming, disarming, opening/closing, landing, taking off, pausing
        missions, connecting, returning, and pushing missions. Additionally, it maps buttons
        for setting and getting UAV flight information, updating settings, and handling
        navigation to different pages.

        The method uses lambda functions to create asynchronous tasks for each button click
        event, ensuring that the UAV functions are executed asynchronously.

        Buttons mapped:
        - Arm
        - Disarm
        - Open/Close
        - Landing
        - Take Off
        - Pause Mission
        - Connect
        - Return
        - Mission
        - Push Mission
        - Set Flight Info (for each UAV)
        - Get Flight Info (for each UAV)
        - Update Settings (for 'settings' and 'overview' pages)
        - Go To (for 'settings' and 'overview' pages)

        Args:
            None

        Returns:
            None
        """
        self.ui.btn_arm.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_arm(self.active_tab_index))
        )

        self.ui.btn_disarm.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_disarm(self.active_tab_index))
        )

        self.ui.btn_open_close.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_openClose(self.active_tab_index))
        )

        self.ui.btn_landing.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_landing(self.active_tab_index))
        )

        self.ui.btn_takeOff.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_takeoff(self.active_tab_index))
        )

        self.ui.btn_pause.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_pauseMission(self.active_tab_index))
        )

        self.ui.btn_connect.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_connect(self.active_tab_index))
        )

        self.ui.btn_rtl.clicked.connect(
            lambda: asyncio.create_task(
                self.uav_fn_return(self.active_tab_index, rtl=True)
            )
        )

        self.ui.btn_return.clicked.connect(
            lambda: asyncio.create_task(
                self.uav_fn_return(self.active_tab_index, rtl=False)
            )
        )

        self.ui.btn_mission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_mission(self.active_tab_index))
        )

        self.ui.btn_pushMission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_pushMission(self.active_tab_index))
        )

        self.ui.btn_toggle_camera.clicked.connect(self.uav_fn_toggle_camera)

        for i, btn in enumerate(self.uav_set_param_buttons):
            btn.clicked.connect(
                lambda uav_index=i + 1: asyncio.create_task(
                    self.uav_fn_set_flight_info(uav_index)
                )
            )

        for i, btn in enumerate(self.uav_get_param_buttons):
            btn.clicked.connect(
                lambda uav_index=i + 1: asyncio.create_task(
                    self.uav_fn_get_flight_info(uav_index=uav_index, copy=True)
                )
            )

        # all is update table
        self.ui.btn_sett_cf_nSwarms.clicked.connect(
            lambda: self._modify_tables(mode="settings")
        )
        self.ui.btn_ovv_cf_nSwarms.clicked.connect(
            lambda: self._modify_tables(mode="overview")
        )

        # go to buttons
        for i, buttons in enumerate(
            zip(self.uav_sett_goTo_buttons, self.uav_ovv_goTo_buttons)
        ):
            buttons[0].clicked.connect(
                lambda uav_index=i: asyncio.create_task(
                    self.uav_fn_goTo(uav_index, "settings")
                )
            )
            buttons[1].clicked.connect(
                lambda uav_index=i: asyncio.create_task(
                    self.uav_fn_goTo(uav_index, "overview")
                )
            )

    def _line_edit_event(self) -> None:
        """
        Maps the returnPressed event of QLineEdit widgets to the process_command coroutine.

        This method iterates over a range of UAV indices and connects the returnPressed signal
        of each QLineEdit widget in the uav_update_commands list to a lambda function. The lambda
        function creates an asyncio task that calls the process_command coroutine with the corresponding
        UAV index.

        Args:
            None

        Returns:
            None
        """
        for index in range(MAX_UAV_COUNT):
            self.uav_update_commands[index].returnPressed.connect(
                lambda uav_index=index + 1: asyncio.create_task(
                    self.process_command(uav_index)
                )
            )

    def _create_streaming_threads(self) -> None:
        """
        Connects the `change_pixmap_signal` of each UAV view thread to the `update_uav_screen_view` method.

        This method iterates over a range defined by `MAX_UAV_COUNT` and sets up a connection for each UAV view thread.
        The connection is made such that when the `change_pixmap_signal` is emitted, the `update_uav_screen_view`
        method is called with the corresponding UAV index.

        Args:
            None

        Returns:
            None
        """
        global UAVs
        for index in range(MAX_UAV_COUNT):
            uav_index = index + 1
            if (
                UAVs[uav_index]["streaming_enable"]
                and UAVs[uav_index]["connection_allow"]
            ):
                self.uav_stream_threads[index] = Thread(
                    target=self.stream_on_uav_screen,
                    args=(uav_index,),
                    name=f"UAV-{uav_index}",
                )
                self.uav_stream_captures[index] = cv2.VideoCapture(
                    UAVs[uav_index]["streaming_address"]
                )
                print(f"UAV-{uav_index} streaming thread created.")
        pass

    def uav_fn_toggle_camera(self) -> None:
        """
        Toggles the camera view for all UAVs.

        This method iterates through all UAVs up to the maximum count defined by
        MAX_UAV_COUNT and starts the camera view thread for each UAV.

        Toggles the camera view for a specified UAV index.

        Args:
            None`

        Returns:
            None
        """
        try:
            for uav_index in range(1, MAX_UAV_COUNT + 1):
                if UAVs[uav_index]["streaming_enable"]:
                    self.uav_stream_threads[uav_index - 1].start()
                    self.uav_stream_threads[
                        uav_index - 1
                    ].join()  # add this for join the thread queue
                    print(f"UAV-{uav_index} streaming thread started.")
        except Exception as e:
            print(f"Error: {repr(e)}")
            self.popup_msg("Error", str(e))

    # //-/////////////////////////////////////////////////////////////

    def _switch_tab(self, index) -> None:
        """
        Switch the active tab using the tab bar.

        Args:
            index (int): The index of the tab to switch to.

        Returns:
            None
        """
        self.active_tab_index = index
        self.active_stack_index = self.ui.stackedWidget.currentIndex()

    def _switch_layout(self, stack_name, tab_name) -> None:
        """
        Switch the active tab and stack using the menu bar.

        Args:
            stack_name (str): The name of the stack to switch to.
            tab_name (str): The name of the tab to switch to.

        Returns:
            None
        """
        self.ui.stackedWidget.setCurrentIndex(stackedWidget_indexes[stack_name])
        self.ui.tabWidget.setCurrentIndex(tabWidget_indexes[tab_name])

        self.active_tab_index = self.ui.tabWidget.currentIndex()
        self.active_stack_index = self.ui.stackedWidget.currentIndex()

    def _handling_checkBoxes(self, mode="init") -> list:
        """
        Handle the state of checkboxes and update UAV detection settings.

        Args:
            mode (str): The page context ('init', 'settings' or 'overview').

        Returns:
            list: A list of indices of checked checkboxes.
        """
        if mode == "init":
            for i, widget in enumerate(self.sett_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["streaming_enable"])
            for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["streaming_enable"])
            for i, widget in enumerate(self.sett_checkBox_active_lists):
                widget.setChecked(UAVs[i + 1]["connection_allow"])
        elif mode == "settings":
            for i, widget in enumerate(self.sett_checkBox_detect_lists):
                UAVs[i + 1]["streaming_enable"] = widget.isChecked()
        elif mode == "overview":
            for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                UAVs[i + 1]["streaming_enable"] = widget.isChecked()

        results = []
        for i, widget in enumerate(self.sett_checkBox_active_lists):
            UAVs[i + 1]["connection_allow"] = widget.isChecked()
            if widget.isChecked():
                results.append(i + 1)
        return results

    def _modify_tables(self, mode="init") -> None:
        """
        Update settings based on the checked checkboxes and table values.

        Args:
            mode (str): The page context ('init', 'settings' or 'overview').

        Returns:
            None
        """
        try:
            headers = ["id", "connection_address", "streaming_address"]
            if mode != "init":
                checked_uav_indexes = self._handling_checkBoxes(mode=mode)

                if mode == "settings":
                    nSwarms = min(
                        int(self.ui.nSwarms_sett.value()), len(checked_uav_indexes)
                    )
                    dataFrame_widget = get_values_from_table(
                        self.ui.table_uav_large, headers=headers
                    )
                else:
                    nSwarms = min(
                        int(self.ui.nSwarms_ovv.value()), len(checked_uav_indexes)
                    )
                    dataFrame_widget = get_values_from_table(
                        self.ui.table_uav_small, headers=headers
                    )

                self.ui.nSwarms_sett.setValue(nSwarms)
                self.ui.nSwarms_ovv.setValue(nSwarms)

                draw_table(
                    self.ui.table_uav_large,
                    data=dataFrame_widget,
                    indexes=checked_uav_indexes[:nSwarms],
                    headers=headers,
                )
                draw_table(
                    self.ui.table_uav_small,
                    data=dataFrame_widget,
                    indexes=checked_uav_indexes[:nSwarms],
                    headers=headers,
                )
                # update UAVs values according to the table
                for i in range(1, MAX_UAV_COUNT + 1):
                    if i in checked_uav_indexes:
                        UAVs[i]["system_address"], port = dataFrame_widget[
                            "connection_address"
                        ][i - 1].split("-p")
                        # UAVs[i]['system']._port = int(port)
                        UAVs[i]["streaming_address"] = dataFrame_widget[
                            "streaming_address"
                        ][i - 1].split("VIDEO: ")[1]
                print("[INFO] Updated UAVs values according to the table")
            else:
                data = {
                    headers[0]: [i for i in range(1, MAX_UAV_COUNT + 1)],
                    headers[1]: [
                        f"{UAVs[i]['system_address']} -p {UAVs[i]['system']._port}"
                        for i in range(1, MAX_UAV_COUNT + 1)
                    ],
                    headers[2]: [
                        f"VIDEO: {UAVs[i]['streaming_address']}"
                        for i in range(1, MAX_UAV_COUNT + 1)
                    ],
                }
                if mode == "init":
                    indexes = [i for i in range(1, MAX_UAV_COUNT + 1)]
                else:
                    indexes = [
                        i
                        for i in range(1, MAX_UAV_COUNT + 1)
                        if UAVs[i]["uav_information"]["connection_status"]
                    ]

                draw_table(
                    self.ui.table_uav_large,
                    data=pd.DataFrame.from_dict(data),
                    indexes=indexes,
                    headers=headers,
                )
                draw_table(
                    self.ui.table_uav_small,
                    data=pd.DataFrame.from_dict(data),
                    indexes=indexes,
                    headers=headers,
                )

        except Exception as e:
            self.popup_msg(
                f"Error: {repr(e)}", src_msg="_modify_tables", type_msg="error"
            )

    # ////////////////////////////////////////////////////////////////

    async def process_command(self, uav_index) -> None:
        """
        Processes a command for a UAV based on the given index.

        Args:
            uav_index (int): The index of the UAV to process the command for.

        Returns:
            None

        Raises:
            Exception: If the input command is invalid.

        The method retrieves the command text from the UAV update commands list,
        parses it to extract the command and value, and then executes the corresponding
        action for the UAV. Supported commands include 'forward', 'backward', 'left',
        'right', 'up', and 'down'. The UAV will move the specified distance in the
        given direction. After processing the command, the input field is cleared.
        If an invalid command is provided, an error message is displayed.
        """
        try:
            text = self.uav_update_commands[uav_index - 1].text()
            # TODO: if command <do something more here>

            if text.lower().strip() == "hold":
                await UAVs[uav_index]["system"].action.hold()
            else:
                command, value = str(text).split("=")
                command = command.strip().lower()
                value = value.strip().lower()
                print(f"Command: {command}, Value: {value}")
                if command in ["forward", "backward", "left", "right", "up", "down"]:
                    distance = float(value)
                    await self.uav_fn_goTo_distance(
                        self.active_tab_index, command, distance
                    )
                    await UAVs[uav_index]["system"].action.hold()
                # Clear the input after processing the command
                self.uav_update_commands[uav_index - 1].clear()

        except Exception as e:
            self.popup_msg(
                f"Invalid input: {repr(e)}", src_msg="process_command", type_msg="error"
            )

    # ////////////////////////////////////////////////////////////////
    # ? UAV functions with buttons
    async def uav_fn_connect(self, uav_index) -> None:
        """
        Asynchronously connects to a UAV or all UAVs.

        This function attempts to establish a connection to a specified UAV by its index.
        If the index is 0, it will attempt to connect to all UAVs.

        Args:
            uav_index (int): The index of the UAV to connect to. If 0, connects to all UAVs.

        Returns:
            None

        Raises:
            Exception: If there is an error during the connection process, an exception is raised and a popup message is displayed.
        """
        global UAVs
        try:
            if uav_index != 0:
                if UAVs[uav_index]["connection_allow"]:
                    self.update_terminal(
                        f"[INFO] Sent CONNECT command to UAV {uav_index}"
                    )

                    # default is not connected
                    UAVs[uav_index]["uav_information"]["connection_status"] = False
                    UAVs[uav_index]["label_param"].setStyleSheet(
                        "background-color: red"
                    )
                    self.sett_checkBox_active_lists[uav_index - 1].setChecked(False)
                    set_row_color(
                        self.ui.table_uav_large,
                        uav_index - 1,
                        QtGui.QColor(255, 160, 122),
                    )
                    set_row_color(
                        self.ui.table_uav_small,
                        uav_index - 1,
                        QtGui.QColor(255, 160, 122),
                    )

                    await UAVs[uav_index]["system"].connect(
                        system_address=UAVs[uav_index]["system_address"]
                    )

                    UAVs[uav_index]["uav_information"]["connection_status"] = True

                    UAVs[uav_index]["information_view"].setText(
                        self.template_information(
                            uav_index, **UAVs[uav_index]["uav_information"]
                        )
                    )

                    await self.uav_fn_check_connection(uav_index)

                else:
                    self.update_terminal(
                        f"[INFO] Connection not allowed for UAV {uav_index}"
                    )

            else:
                connect_all_UAVs = [
                    self.uav_fn_connect(i) for i in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*connect_all_UAVs)

        except Exception as e:
            self.popup_msg(
                f"Connection error: {repr(e)}",
                src_msg="uav_fn_connect",
                type_msg="error",
            )

    async def uav_fn_arm(self, uav_index) -> None:
        """
        Arms the UAV specified by the given index. If the index is 0, it will arm all UAVs.

        Args:
            uav_index (int): The index of the UAV to arm. If 0, all UAVs will be armed.

        Returns:
            None

        Raises:
            Exception: If there is an issue with connecting to or arming the UAV.

        Notes:
            - The function updates the terminal with the status of the arm command.
            - It connects to the UAV system and sends the arm command.
            - After arming, it waits for 3 seconds and then disarms the UAV.
            - The connection status and arming status of the UAV are updated accordingly.
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                self.update_terminal(f"[INFO] Sent ARM command to UAV {uav_index}")
                # # await asyncio.sleep(1)
                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )
                await UAVs[uav_index]["system"].action.arm()
                await asyncio.sleep(3)
                await self.uav_fn_disarm(uav_index)
                # UAVs[uav_index]['uav_information']['connection_status'] = True
                UAVs[uav_index]["uav_information"]["arming_status"] = "ARMED"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            arm_all_UAVs = [self.uav_fn_arm(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*arm_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    async def uav_fn_disarm(self, uav_index) -> None:
        """
        Disarms a specific UAV or all UAVs.

        This asynchronous method sends a DISARM command to a specified UAV if its
        connection status is active. If the uav_index is 0, it will attempt to disarm
        all UAVs.

        Args:
            uav_index (int): The index of the UAV to disarm. If 0, disarms all UAVs.

        Returns:
            None
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                self.update_terminal(f"[INFO] Sent DISARM command to UAV {uav_index}")

                # await asyncio.sleep(1)
                await UAVs[uav_index]["system"].action.disarm()

                UAVs[uav_index]["uav_information"]["arming_status"] = "DISARMED"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            disarm_all_UAVs = [
                self.uav_fn_disarm(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*disarm_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    async def uav_fn_takeoff(self, uav_index) -> None:
        """
        Initiates the takeoff sequence for a specified UAV or all UAVs.

        Args:
            uav_index (int): The index of the UAV to take off. If 0, all UAVs will take off.

        Returns:
            None

        Raises:
            Exception: If there is an issue with the UAV connection or takeoff process.

        Behavior:
            - If uav_index is not 0, it sends a TAKEOFF command to the specified UAV.
            - Connects to the UAV system, arms it, sets the takeoff altitude, and initiates takeoff.
            - Updates the UAV's current information and mode status to 'TAKING OFF'.
            - If uav_index is 0, it initiates the takeoff sequence for all UAVs concurrently.
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                self.update_terminal(f"[INFO] Sent TAKEOFF command to UAV {uav_index}")

                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )
                await UAVs[uav_index]["system"].action.arm()
                await UAVs[uav_index]["system"].action.set_takeoff_altitude(
                    UAVs[uav_index]["uav_information"]["init_height"]
                )
                await UAVs[uav_index]["system"].action.takeoff()

                # # update initial position of UAV
                UAVs[uav_index]["uav_information"]["init_latitude"] = UAVs[uav_index][
                    "uav_information"
                ]["position_status"][0]
                UAVs[uav_index]["uav_information"]["init_longitude"] = UAVs[uav_index][
                    "uav_information"
                ]["position_status"][1]

                # update UAV information
                UAVs[uav_index]["uav_information"]["connection_status"] = True
                UAVs[uav_index]["uav_information"]["mode_status"] = "TAKING OFF"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            takeoff_all_UAVs = [
                self.uav_fn_takeoff(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*takeoff_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    async def uav_fn_landing(self, uav_index) -> None:
        """
        Asynchronously commands a UAV to land.

        This function sends a landing command to a specified UAV or to all UAVs if the index is 0.
        It updates the terminal with the landing status, sends the landing command, disarms the UAV,
        and updates the UAV's mode status to 'LANDING'.

        Args:
            uav_index (int): The index of the UAV to land. If 0, all UAVs will be commanded to land.

        Returns:
            None
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                self.update_terminal(f"[INFO] Sent LANDING command to UAV {uav_index}")

                # await asyncio.sleep(1)
                await UAVs[uav_index]["system"].action.land()

                UAVs[uav_index]["uav_information"]["mode_status"] = "LANDING"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            landing_all_UAVs = [
                self.uav_fn_landing(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*landing_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    async def uav_fn_return(self, uav_index, rtl=False) -> None:
        """
        Asynchronously pauses the mission of a UAV or all UAVs.

        This function sends a pause command to a specific UAV identified by `uav_index`.
        If `uav_index` is 0, it sends the command to all UAVs. The function updates the terminal
        with the status and handles exceptions by displaying a popup message.

        Args:
            uav_index (int): The index of the UAV to command. If 0, commands all UAVs.
            rtl (bool, optional): If True, sends a Return-To-Launch (RTL) command. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If there is an error in sending the pause command.
        """
        global UAVs
        try:
            if uav_index != 0:
                if (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):
                    if rtl:
                        self.update_terminal(
                            f"[INFO] Sent RTL command to UAV {uav_index}"
                        )
                        # await asyncio.sleep(1)
                        init_longitude = UAVs[uav_index]["uav_information"][
                            "init_longitude"
                        ]
                        init_latitude = UAVs[uav_index]["uav_information"][
                            "init_latitude"
                        ]
                        current_longitude = UAVs[uav_index]["uav_information"][
                            "position_status"
                        ][1]
                        current_latitude = UAVs[uav_index]["uav_information"][
                            "position_status"
                        ][0]
                        if (init_longitude == current_longitude) and (
                            init_latitude == current_latitude
                        ):
                            self.update_terminal(
                                f"[INFO] UAV {uav_index} is already at the initial position, landing..."
                            )
                            await UAVs[uav_index]["system"].action.land()
                        else:
                            await UAVs[uav_index][
                                "system"
                            ].action.set_return_to_launch_altitude(
                                UAVs[uav_index]["uav_information"]["init_height"]
                            )
                            await UAVs[uav_index]["system"].action.return_to_launch()

                        UAVs[uav_index]["uav_information"]["mode_status"] = "RTL"
                        UAVs[uav_index]["information_view"].setText(
                            self.template_information(
                                uav_index, **UAVs[uav_index]["uav_information"]
                            )
                        )
                    else:
                        self.update_terminal(
                            f"[INFO] Sent RETURN command to UAV {uav_index} \
                                to lat: {UAVs[uav_index]['uav_information']['init_latitude']} \
                                    long: {UAVs[uav_index]['uav_information']['init_longitude']}"
                        )
                        # await asyncio.sleep(1)
                        await self.uav_fn_goTo_position(
                            uav_index,
                            latitude=UAVs[uav_index]["uav_information"][
                                "init_latitude"
                            ],
                            longitude=UAVs[uav_index]["uav_information"][
                                "init_longitude"
                            ],
                        )

                        UAVs[uav_index]["uav_information"]["mode_status"] = "Return"
                        UAVs[uav_index]["information_view"].setText(
                            self.template_information(
                                uav_index, **UAVs[uav_index]["uav_information"]
                            )
                        )

                else:
                    pass
            elif uav_index == 0:
                return_all_UAVs = [
                    self.uav_fn_return(i, rtl=rtl) for i in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*return_all_UAVs)
            else:
                self.popup_msg("Buttons are disabled on this tab")
        except Exception as e:
            self.popup_msg(
                f"Return error: {repr(e)}", src_msg="uav_fn_return", type_msg="error"
            )

    async def uav_fn_mission(self, uav_index) -> None:
        """
        Executes a mission for a specified UAV or all UAVs if uav_index is 0.

        Args:
            uav_index (int): The index of the UAV to execute the mission for. If 0, the mission is executed for all UAVs.

        Returns:
            None

        Raises:
            Exception: If there is an error during the mission execution.

        The function performs the following steps:
        1. Checks if the UAV is connected.
        2. Reads mission points from a file and creates mission items.
        3. Uploads the mission to the UAV.
        4. Arms the UAV and starts the mission.
        5. Monitors mission progress and initiates return to launch upon mission completion.
        6. Updates the UAV's mode status and information view.
        7. If uav_index is 0, executes the mission for all UAVs concurrently.
        """
        global UAVs
        try:
            if uav_index != 0:
                if (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):

                    self.update_terminal(
                        f"[INFO] Sent MISSION command to UAV {uav_index}"
                    )

                    # NOTE: push mission

                    mission_items = []
                    # Assign hight for mission
                    height = UAVs[uav_index]["uav_information"]["init_height"]
                    # read mission points from file
                    with open(
                        f"{parent_dir}/logs/points/points{uav_index}.txt", "r"
                    ) as file:
                        for line in file:
                            latitude, longitude = map(float, line.strip().split(", "))
                            mission_item_1 = MissionItem(
                                latitude,
                                longitude,
                                height,
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
                            mission_items.append(mission_item_1)
                    mission_plan = MissionPlan(mission_items)
                    await asyncio.sleep(1)
                    # set return to launch after mission
                    await UAVs[uav_index][
                        "system"
                    ].mission.set_return_to_launch_after_mission(True)
                    # upload mission
                    await UAVs[uav_index]["system"].mission.upload_mission(mission_plan)

                    # NOTE: Perform mission

                    await UAVs[uav_index]["system"].action.arm()
                    await UAVs[uav_index]["system"].mission.start_mission()
                    async for mission_progress in UAVs[uav_index][
                        "system"
                    ].mission.mission_progress():
                        if mission_progress.current == mission_progress.total:
                            await self.uav_fn_return(uav_index)
                            break

                    UAVs[uav_index]["uav_information"]["mode_status"] = "Mission"
                    UAVs[uav_index]["information_view"].setText(
                        self.template_information(
                            uav_index, **UAVs[uav_index]["uav_information"]
                        )
                    )
                else:
                    pass
            elif uav_index == 0:
                mission_all_UAVs = [
                    self.uav_fn_mission(i) for i in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*mission_all_UAVs)
            else:
                self.popup_msg("Buttons are disabled on this tab")
        except Exception as e:
            self.popup_msg(
                f"Mission error: {repr(e)}", src_msg="uav_fn_mission", type_msg="error"
            )

    async def uav_fn_pushMission(self, uav_index) -> None:
        """
        Pushes a mission to a specified UAV or all UAVs if uav_index is 0.

        This function reads mission points from a file and uploads them to the specified UAV.
        If uav_index is 0, the mission is pushed to all UAVs.

        Args:
            uav_index (int): The index of the UAV to push the mission to. If 0, the mission is pushed to all UAVs.

        Raises:
            Exception: If there is an error during the mission push process, an exception is raised and a popup message is displayed.

        Notes:
            - The function checks the connection status of the UAV before attempting to push the mission.
            - The mission points are read from a file selected by the user.
            - The mission is uploaded to the UAV and the return to launch after mission is set.
            - The mode status of the UAV is updated to 'Mission pushing'.
        """
        global UAVs
        try:
            if uav_index != 0:
                if (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):

                    self.update_terminal(
                        f"[INFO] Sent PUSH MISSION command to UAV {uav_index}"
                    )

                    # await asyncio.sleep(1)
                    fpath = QFileDialog.getOpenFileName(
                        self,
                        "Open file",
                        f"{parent_dir}/logs/points/",
                        "Files (*.TXT *.txt)",
                    )[0]

                    with open(fpath, "r") as f:
                        file_content = f.read()
                        print("File content:", file_content)

                    mission_items = []
                    # Assign hight for mission
                    height = UAVs[uav_index]["uav_information"]["init_height"]
                    # read mission points from file
                    with open(fpath, "r") as file:
                        for line in file:
                            latitude, longitude = map(float, line.strip().split(", "))
                            mission_item_1 = MissionItem(
                                latitude,
                                longitude,
                                height,
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
                            mission_items.append(mission_item_1)
                    mission_plan = MissionPlan(mission_items)
                    await asyncio.sleep(1)
                    # set return to launch after mission
                    await UAVs[uav_index][
                        "system"
                    ].mission.set_return_to_launch_after_mission(True)
                    # upload mission
                    await UAVs[uav_index]["system"].mission.upload_mission(mission_plan)
                    #
                    UAVs[uav_index]["uav_information"][
                        "mode_status"
                    ] = "Mission pushing"
                    UAVs[uav_index]["information_view"].setText(
                        self.template_information(
                            uav_index, **UAVs[uav_index]["uav_information"]
                        )
                    )
                else:
                    pass
            else:
                # pushMission_all_UAVs = [self.uav_fn_pushMission(
                #     i) for i in range(1, MAX_UAV_COUNT + 1)]
                # await asyncio.gather(*pushMission_all_UAVs)
                self.popup_msg("Buttons are disabled on this tab")
        except Exception as e:
            self.popup_msg(
                f"Mission error: {repr(e)}",
                src_msg="uav_fn_pushMission",
                type_msg="error",
            )

    async def uav_fn_pauseMission(self, uav_index) -> None:
        """
        Pauses the mission of a specified UAV or all UAVs if the index is 0.

        Args:
            uav_index (int): The index of the UAV to pause. If 0, pauses all UAVs.

        Returns:
            None

        Raises:
            None

        Notes:
            - Updates the terminal with a message indicating the PAUSE command was sent.
            - Updates the UAV's mode status to 'Mission paused' if the UAV is connected.
            - If uav_index is 0, pauses the mission for all UAVs concurrently.
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                self.update_terminal(f"[INFO] Sent PAUSE command to UAV {uav_index}")
                # await asyncio.sleep(1)
                await UAVs[uav_index]["system"].mission.pause_mission()
                #
                UAVs[uav_index]["uav_information"]["mode_status"] = "Mission paused"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            pauseMission_all_UAVs = [
                self.uav_fn_pauseMission(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*pauseMission_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    async def uav_fn_openClose(self, uav_index) -> None:
        """
        Asynchronously toggles the actuator status of a specified UAV or all UAVs.

        If the `uav_index` is not 0, it sends an OPEN/CLOSE command to the specified UAV.
        If the `uav_index` is 0, it sends the command to all UAVs.

        Args:
            uav_index (int): The index of the UAV to toggle. If 0, toggles all UAVs.

        Returns:
            None
        """
        global UAVs
        if uav_index != 0:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                self.update_terminal(
                    f"[INFO] Sent OPEN/CLOSE command to UAV {uav_index}"
                )
                # await asyncio.sleep(1)
                if UAVs[uav_index]["uav_information"]["actuator_status"]:
                    await UAVs[uav_index]["system"].action.set_actuator(uav_index, 0)
                    UAVs[uav_index]["uav_information"]["actuator_status"] = False
                else:
                    await UAVs[uav_index]["system"].action.set_actuator(uav_index, 1)
                    UAVs[uav_index]["uav_information"]["actuator_status"] = True

                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
            else:
                pass
        elif uav_index == 0:
            openClose_all_UAVs = [
                self.uav_fn_openClose(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*openClose_all_UAVs)
        else:
            self.popup_msg("Buttons are disabled on this tab")

    # //-/////////////////////////////////////////////////////////////
    # ? UAV functions utils

    async def uav_fn_goTo(self, uav_index, page="settings", *args) -> None:
        """
        Handles the UAV navigation to a specified point based on the provided page and UAV index.

        Args:
            uav_index (int): The index of the UAV to navigate. If 0, all UAVs will navigate to the point.
            page (str, optional): The page from which the coordinates are retrieved. Defaults to 'settings'.
            *args: Additional arguments.

        Returns:
            None

        Notes:
            - If the longitude or latitude values are empty, default values are used.
            - The coordinates are updated in the UI fields for both 'settings' and 'overview' pages.
            - If uav_index is 0, all UAVs will navigate to the specified point concurrently.
        """

        default_longitude = (
            UAVs[uav_index]["uav_information"]["init_longitude"] + uav_index * 0.0001
        )
        default_latitude = UAVs[uav_index]["uav_information"]["init_latitude"]

        if page == "settings":
            longitude = self.ui.lineEdit_sett_longitude.text()
            latitude = self.ui.lineEdit_sett_latitude.text()
        else:
            longitude = self.ui.lineEdit_ovv_longitude.text()
            latitude = self.ui.lineEdit_ovv_latitude.text()
        # check if the values are empty
        longitude = float(longitude) if len(longitude) > 0 else default_longitude
        latitude = float(latitude) if len(latitude) > 0 else default_latitude
        #
        self.ui.lineEdit_ovv_longitude.setText(str(longitude))
        self.ui.lineEdit_ovv_latitude.setText(str(latitude))
        self.ui.lineEdit_sett_longitude.setText(str(longitude))
        self.ui.lineEdit_sett_latitude.setText(str(latitude))
        #

        if uav_index != 0:
            print("Go to UAV", uav_index, "to", latitude, longitude)
            await self.uav_fn_goTo_position(
                uav_index, latitude=latitude, longitude=longitude
            )
        else:
            goTo_all_UAVs = [
                self.uav_fn_goTo_position(i, latitude=latitude, longitude=longitude)
                for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*goTo_all_UAVs)

    async def uav_fn_goTo_distance(self, uav_index, direction, distance) -> None:
        """
        Asynchronously moves the UAV to a specified distance in a given direction.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.
            direction (str): The direction to move the UAV. Can be 'forward', 'backward', 'left', 'right', 'up', or 'down'.
            distance (float): The distance to move the UAV in meters.

        Returns:
            None

        Raises:
            KeyError: If the UAV index is not found in the UAVs list.
            ValueError: If the direction is not one of the specified directions.

        Notes:
            - The function calculates the new position based on the current position and the specified distance.
            - The Earth's radius (r_earth) is assumed to be 6378137 meters.
            - The function only moves the UAV if its connection status is active.
            - The function uses the UAV's telemetry data to get the current position and then calculates the new position.
            - The function sends the UAV to the new calculated position using the `goto_location` method.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            # go forward, backward, left, right with distance
            # get current position, calculate new position, and go to that position(point)
            r_earth = 6378137

            lat, lon, alt = 0, 0, 0
            initial_lat, initial_lon, initial_alt = 0, 0, 0
            async for position in UAVs[uav_index]["system"].telemetry.position():
                if initial_lat == 0 and initial_lon == 0 and initial_alt == 0:
                    initial_lat = position.latitude_deg
                    initial_lon = position.longitude_deg
                    initial_alt = position.absolute_altitude_m

                lat = position.latitude_deg
                lon = position.longitude_deg
                alt = position.absolute_altitude_m

                if direction == "forward":
                    lat = initial_lat + (distance / r_earth) * (180 / math.pi)
                elif direction == "backward":
                    lat = initial_lat - (distance / r_earth) * (180 / math.pi)
                elif direction == "left":
                    lon = initial_lon - (
                        distance / (r_earth * math.cos(math.pi * initial_lat / 180))
                    ) * (180 / math.pi)
                elif direction == "right":
                    lon = initial_lon + (
                        distance / (r_earth * math.cos(math.pi * initial_lat / 180))
                    ) * (180 / math.pi)
                elif direction == "up":
                    alt = initial_alt + distance
                elif direction == "down":
                    alt = initial_alt - distance

                print(
                    f"Go from {initial_lat}, {initial_lon}, {initial_alt} to {lat}, {lon}, {alt}"
                )

                await UAVs[uav_index]["system"].action.goto_location(lat, lon, alt, 0)
                break
        else:
            pass

    async def uav_fn_goTo_position(self, uav_index, latitude, longitude, *args) -> None:
        """
        Asynchronously commands a UAV to go to a specified geographic point.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.
            latitude (float): The latitude of the target location.
            longitude (float): The longitude of the target location.
            *args: Additional arguments (not used).

        Returns:
            None

        Behavior:
            - If the UAV's current connection status is active, it retrieves the current altitude
              and commands the UAV to go to the specified latitude and longitude at the current altitude.
            - If the UAV's current connection status is inactive, the function does nothing.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for position in UAVs[uav_index]["system"].telemetry.position():
                height = position.absolute_altitude_m
                await UAVs[uav_index]["system"].action.goto_location(
                    latitude, longitude, height, 0
                )
        else:
            pass

    async def uav_fn_goTo_list_UAVs(self, UAVs_to_control, *args) -> None:
        """
        Asynchronously commands all specified UAVs to go to their respective destinations.

        This method takes a list of UAV indices and uses asyncio.gather to concurrently
        execute the goTo_UAV method for each UAV in the list.

        Args:
            UAVs_to_control (list): A list of indices representing the UAVs to control.
            *args: Additional arguments that may be passed to the method.

        Returns:
            None
        """
        await asyncio.gather(
            *[self.uav_fn_goTo_UAV(uav_index) for uav_index in UAVs_to_control]
        )

    async def uav_fn_goTo_UAV(self, uav_index, *args) -> None:
        """
        Asynchronously directs a UAV to a specified location based on coordinates read from a file.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.
            *args: Additional arguments (not used in this function).

        Returns:
            None

        Behavior:
            - Checks if the UAV at the given index has an active connection.
            - Reads target latitude and longitude from a file located at '{parent_dir}/logs/detect/detect.txt'.
            - Continuously checks the UAV's current position.
            - Commands the UAV to move to the target location if it is not already there.
            - Logs a message when the UAV reaches the target location.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            folder_path = f"{parent_dir}/logs/detect"
            txt_file_path = os.path.join(folder_path, "detect.txt")
            with open(txt_file_path, "r") as file:
                content = file.read()
                lat_detect, lon_detect = map(float, content.strip().split(", "))

            async for position in UAVs[uav_index]["system"].telemetry.position():
                if (
                    abs(position.latitude_deg - lat_detect) < 0.00001
                    and abs(position.longitude_deg - lon_detect) < 0.00001
                ):
                    self.update_terminal(
                        f"[INFO] UAV {uav_index} is at the target location"
                    )
                    break
                height = position.absolute_altitude_m
                await UAVs[uav_index]["system"].action.goto_location(
                    lat_detect, lon_detect, height, 0
                )
        else:
            pass

    # --------------------------<Get status>-----------------------------
    async def uav_fn_get_altitude(self, uav_index) -> None:
        """
        Asynchronously retrieves and updates the altitude and position information of a specified UAV.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.

        Returns:
            None

        Functionality:
            - Checks if the UAV at the given index is connected.
            - If connected, retrieves the UAV's telemetry data including relative altitude, absolute altitude, latitude, and longitude.
            - Updates the UAV's current information with the retrieved telemetry data.
            - Updates the UAV's information view with the new data.
            - Writes the latitude and longitude to a GPS log file.

        Note:
            - The function assumes the existence of a global UAVs list and a parent_dir variable.
            - The telemetry data is retrieved asynchronously.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for position in UAVs[uav_index]["system"].telemetry.position():
                alt_rel = round(position.relative_altitude_m, 2)
                alt_msl = round(position.absolute_altitude_m, 2)
                latitude = round(position.latitude_deg, 6)
                longitude = round(position.longitude_deg, 6)

                # update UAVs information
                UAVs[uav_index]["uav_information"]["altitude_status"] = [
                    alt_rel,
                    alt_msl,
                ]
                UAVs[uav_index]["uav_information"]["position_status"] = [
                    latitude,
                    longitude,
                ]

                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
                with open(f"{parent_dir}/logs/gps/gps_data{uav_index}.txt", "w") as f:
                    f.write(str(latitude) + ", " + str(longitude))
        else:
            pass

    async def uav_fn_get_mode(self, uav_index) -> None:
        """
        Asynchronously retrieves and updates the flight mode status of a UAV.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.

        Returns:
            None

        This function checks the connection status of the UAV specified by `uav_index`.
        If the UAV is connected, it asynchronously iterates over the flight mode telemetry
        data and updates the `mode_status` in the UAV's current information. It also updates
        the information view with the new mode status.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for mode in UAVs[uav_index]["system"].telemetry.flight_mode():
                mode_status = mode
                UAVs[uav_index]["uav_information"]["mode_status"] = mode_status
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
        else:
            pass

    async def uav_fn_get_battery(self, uav_index) -> None:
        """
        Asynchronously retrieves and updates the battery status of a UAV.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.

        Returns:
            None

        This function checks the connection status of the UAV specified by `uav_index`.
        If the UAV is connected, it retrieves the battery status from the telemetry data,
        updates the UAV's current information with the battery status, and updates the
        information view with the new data.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for battery in UAVs[uav_index]["system"].telemetry.battery():
                battery_status = round(battery.remaining_percent * 100, 1)
                UAVs[uav_index]["uav_information"]["battery_status"] = (
                    str(battery_status) + "%"
                )
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
        else:
            pass

    async def uav_fn_get_arm_status(self, uav_index) -> None:
        """
        Asynchronously retrieves and updates the arming status of a UAV.

        This function checks the connection status of the UAV at the specified index.
        If the UAV is connected, it listens for changes in the arming status and updates
        the UAV's current information and the information view accordingly.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.

        Returns:
            None
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for arm_status in UAVs[uav_index]["system"].telemetry.armed():
                arm_status = "ARMED" if arm_status else "DISARMED"
                UAVs[uav_index]["uav_information"]["arming_status"] = arm_status
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
        else:
            pass

    async def uav_fn_get_gps(self, uav_index) -> None:
        """
        Asynchronously retrieves GPS information for a specified UAV and updates its status.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.

        Returns:
            None

        Behavior:
            - Checks if the UAV at the given index has an active connection.
            - If connected, asynchronously iterates over the GPS information stream.
            - Updates the UAV's current GPS status.
            - Updates the UAV's information view with the latest GPS status.
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for gps in UAVs[uav_index]["system"].telemetry.gps_info():
                gps_status = gps.fix_type
                UAVs[uav_index]["uav_information"]["gps_status"] = gps_status
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(
                        uav_index, **UAVs[uav_index]["uav_information"]
                    )
                )
        else:
            pass

    async def uav_fn_get_flight_info(self, uav_index, copy=False) -> None:
        """
        Asynchronously retrieves flight information parameters for a specified UAV and updates the display.

        Args:
            uav_index (int): The index of the UAV to retrieve flight information for.
            copy (bool, optional): If True, copies the retrieved parameters to another set of display fields. Defaults to False.

        Returns:
            None

        Raises:
            None

        Notes:
            - The function retrieves various flight parameters such as takeoff altitude, disarm land command,
              takeoff speed, landing speed, and several control parameters.
            - If the UAV is not connected, a warning message is displayed in the terminal.
        """
        global UAVs
        try:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                parameters = {}
                parameters["MIS_TAKEOFF_ALT"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MIS_TAKEOFF_ALT")
                parameters["COM_DISARM_LAND"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("COM_DISARM_LAND")
                parameters["MPC_TKO_SPEED"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MPC_TKO_SPEED")
                parameters["MPC_LAND_SPEED"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MPC_LAND_SPEED")
                parameters["MPC_XY_P"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MPC_XY_P")
                parameters["MPC_XY_VEL_D_ACC"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MPC_XY_VEL_D_ACC")
                parameters["MPC_XY_VEL_P_ACC"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MPC_XY_VEL_P_ACC")
                parameters["MC_PITCH_P"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MC_PITCH_P")
                parameters["MC_ROLL_P"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MC_ROLL_P")
                parameters["MC_YAW_P"] = await UAVs[uav_index][
                    "system"
                ].param.get_param_float("MC_YAW_P")

                for i, (_, value) in enumerate(parameters.items()):
                    UAVs[uav_index]["param_display"].children()[i + 1].setText(
                        str(round(value, 1))
                    )

                if copy:
                    for i, (_, value) in enumerate(parameters.items()):
                        UAVs[uav_index]["param_set"].children()[i + 1].setText(
                            str(round(value, 1))
                        )
            else:
                self.update_terminal(
                    f"[WARNING] UAV {uav_index} is not connected, cannot get flight information"
                )
        except Exception as e:
            self.popup_msg(
                f"Get flight info error: {repr(e)}",
                src_msg="uav_fn_get_flight_info",
                type_msg="error",
            )

    async def uav_fn_set_flight_info(self, uav_index) -> None:
        """
        Asynchronously sets the flight parameters for a specified UAV.

        This function updates various flight parameters for the UAV identified by `uav_index`.
        It retrieves the new parameter values from the UAV's parameter set and updates the UAV's system
        with these values. If a parameter value is not provided, it uses the existing value from the UAV's
        parameter display.

        Parameters:
        uav_index (int): The index of the UAV whose flight parameters are to be set.

        Returns:
        None

        Preconditions:
        - The UAV's current connection status must be True.

        Post conditions:
        - The UAV's flight parameters are updated with the new values.
        - The UAV's flight information is retrieved after updating the parameters.
        """
        global UAVs
        try:
            if (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):

                parameters = {}
                parameter_list = [
                    "MIS_TAKEOFF_ALT",
                    "COM_DISARM_LAND",
                    "MPC_TKO_SPEED",
                    "MPC_LAND_SPEED",
                    "MPC_XY_P",
                    "MPC_XY_VEL_P_ACC",
                    "MPC_XY_VEL_D_ACC",
                    "MC_PITCH_P",
                    "MC_ROLL_P",
                    "MC_YAW_P",
                ]
                for i, (new_value, value) in enumerate(
                    zip(
                        UAVs[uav_index]["param_set"].children()[1:-1],
                        UAVs[uav_index]["param_display"].children()[1:-1],
                    )
                ):
                    if new_value.text() == "":
                        parameters[parameter_list[i]] = value.text()
                    else:
                        parameters[parameter_list[i]] = float(new_value.text())

                await UAVs[uav_index]["system"].param.set_param_float(
                    "MPC_TKO_SPEED", parameters["MPC_TKO_SPEED"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MPC_LAND_SPEED", parameters["MPC_LAND_SPEED"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "COM_DISARM_LAND", parameters["COM_DISARM_LAND"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MC_YAW_P", parameters["MC_YAW_P"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MC_ROLL_P", parameters["MC_ROLL_P"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MC_PITCH_P", parameters["MC_PITCH_P"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MPC_XY_P", parameters["MPC_XY_P"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MPC_XY_VEL_P_ACC", parameters["MPC_XY_VEL_P_ACC"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MPC_XY_VEL_D_ACC", parameters["MPC_XY_VEL_D_ACC"]
                )
                await UAVs[uav_index]["system"].param.set_param_float(
                    "MIS_TAKEOFF_ALT", parameters["MIS_TAKEOFF_ALT"]
                )

                await self.uav_fn_get_flight_info(uav_index=uav_index, copy=False)
            else:
                pass
        except Exception as e:
            self.popup_msg(
                f"Set flight info error: {repr(e)}",
                src_msg="uav_fn_set_flight_info",
                type_msg="error",
            )

    async def uav_fn_check_connection(self, uav_index) -> None:
        """
        Asynchronously checks the connection status of a UAV and performs various setup tasks.

        Args:
            uav_index (int): The index of the UAV to check the connection for.

        Returns:
            None

        This function performs the following steps:
        1. Waits for the UAV to connect and updates the terminal and UI based on the connection status.
        2. Checks if the global position estimate is good enough for flying.
        3. If the UAV is connected, sets the maximum speed, retrieves all parameters, and writes them to a log file.
        4. Gathers various telemetry data such as altitude, mode, battery status, arm status, GPS, and flight information.

        Note:
            The function assumes that the UAVs dictionary and the update_terminal method are defined elsewhere in the code.
        """
        global UAVs
        print(f"Waiting for drone {uav_index} to connect...")
        async for state in UAVs[uav_index]["system"].core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone {uav_index}!")
                self.update_terminal(
                    f"[INFO] Received CONNECT signal from UAV {uav_index}"
                )
                UAVs[uav_index]["label_param"].setStyleSheet("background-color: green")
                self.sett_checkBox_active_lists[uav_index - 1].setChecked(True)
                set_row_color(
                    self.ui.table_uav_large, uav_index - 1, QtGui.QColor(144, 238, 144)
                )
                set_row_color(
                    self.ui.table_uav_small, uav_index - 1, QtGui.QColor(144, 238, 144)
                )
            break

        # Checking if Global Position Estimate is ok
        async for health in UAVs[uav_index]["system"].telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position state is good enough for flying.")
                break
        #
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            await UAVs[uav_index]["system"].action.set_maximum_speed(1.0)

            # Get the list of parameters
            all_params = await UAVs[uav_index]["system"].param.get_all_params()

            with open(f"{parent_dir}/logs/params/params{uav_index}.txt", "w") as f:

                for param in all_params.int_params:
                    f.write(f"{param.name}: {param.value}\n")

                for param in all_params.float_params:
                    f.write(f"{param.name}: {param.value}\n")
            #
            await asyncio.gather(
                self.uav_fn_printStatus(uav_index),
                self.uav_fn_get_altitude(uav_index),
                self.uav_fn_get_mode(uav_index),
                self.uav_fn_get_battery(uav_index),
                self.uav_fn_get_arm_status(uav_index),
                self.uav_fn_get_gps(uav_index),
                self.uav_fn_get_flight_info(uav_index, copy=False),
            )
        else:
            pass

    async def uav_fn_printStatus(self, uav_index) -> None:
        """
        Asynchronously prints the status of a UAV to the terminal.

        This function checks the connection status of a UAV specified by the
        `uav_index`. If the UAV is connected, it retrieves status text messages
        from the UAV's telemetry system and updates the terminal with these messages.

        Args:
            uav_index (int): The index of the UAV in the global UAVs list.

        Returns:
            None
        """
        global UAVs
        if (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):

            async for status in UAVs[uav_index]["system"].telemetry.status_text():
                status = f"> {status.type} - {status.text}"
                self.update_terminal(status, uav_index)
        else:
            pass

    # //-/////////////////////////////////////////////////////////////
    async def compareDistance(self, num_UAVs, *args) -> None:
        """
        Compares the distance of multiple UAVs to a detected location and directs the closest ones to move.

        Args:
            num_UAVs (int): The number of UAVs to compare and control.
            *args: Additional arguments (not used in this function).

        Returns:
            None

        The function reads the detected location from a file, retrieves the current positions of the specified number of UAVs,
        calculates the distance of each UAV to the detected location, sorts the UAVs by distance, and directs the closest ones to move.
        """
        global UAVs
        if num_UAVs <= 0:
            return
        folder_path = f"{parent_dir}/logs/detect"
        txt_file_path = os.path.join(folder_path, "detect.txt")
        with open(txt_file_path, "r") as file:
            content = file.read()
            lat_detect, lon_detect = map(float, content.strip().split(", "))

        latitudes = []
        longitudes = []

        for drone in list(UAVs.values())[:num_UAVs]:
            async for position in drone["system"].telemetry.position():
                latitudes.append(position.latitude_deg)
                longitudes.append(position.longitude_deg)

        if not latitudes or not longitudes:
            return

        distances = []
        for i in range(num_UAVs):
            distances.append(
                calculate_distance(latitudes[i], longitudes[i], lat_detect, lon_detect)
            )

        sorted_UAVs_index = sorted(range(len(distances)), key=lambda k: distances[k])
        UAVs_to_control = sorted_UAVs_index[:num_UAVs]
        await self.goTo_all_UAVs(UAVs_to_control)

    # //-/////////////////////////////////////////////////////////////
    # ? display view functions

    # @pyqtSlot(int)
    def stream_on_uav_screen(self, uav_index) -> None:
        """
        Updates the UAV screen view with the specified UAV's information.

        Args:
            uav_index (int): The index of the UAV to update the screen view for.

        Returns:
            None
        """
        try:
            global UAVs
            current_tab = self.ui.tabWidget.currentIndex()

            if UAVs[uav_index]["uav_information"]["connection_status"]:
                if UAVs[uav_index]["streaming_enable"]:

                    if UAVs[uav_index]["uav_information"]["streaming_status"]:
                        UAVs[uav_index]["uav_information"]["streaming_status"] = False
                        # self.ui.btn_toggle_camera.setText("Start Camera")
                        # self.ui.btn_toggle_camera.setStyleSheet(
                        #     "background-color: rgb(0, 255, 0);"
                        # )
                    else:
                        UAVs[uav_index]["uav_information"]["streaming_status"] = True
                        # self.ui.btn_toggle_camera.setText("Stop Camera")
                        # self.ui.btn_toggle_camera.setStyleSheet(
                        #     "background-color: rgb(255, 0, 0);"
                        # )

                    is_opened = self.uav_stream_captures[uav_index - 1].isOpened()

                    while is_opened:
                        ret, frame = self.uav_stream_captures[uav_index - 1].read()
                        # print(f"UAV {uav_index} streaming status: {ret}")
                        print(frame.shape)
                        if ret:
                            self.update_uav_screen_view(uav_index, frame)
                        else:
                            self.uav_stream_captures[uav_index - 1].set(
                                cv2.CAP_PROP_POS_FRAMES, 0
                            )

                        key = cv2.waitKey(1) & 0xFF
                        if not UAVs[uav_index]["uav_information"]["streaming_status"]:
                            break
                    self.uav_stream_captures[uav_index - 1].release()
        except Exception as e:
            self.popup_msg(
                f"Stream on UAV screen error: {repr(e)}",
                src_msg="stream_on_uav_screen",
                type_msg="error",
            )

    def update_uav_screen_view(self, uav_index, frame) -> None:
        """
        Starts streaming video from the specified UAV to the screen view.

        Args:
            uav_index (int): The index of the UAV to start streaming video from.

        Returns:
            None
        """
        try:
            global UAVs
            for screen in screen_sizes.keys():
                UAVs[uav_index][screen].setPixmap(
                    convert_cv2qt(frame, size=screen_sizes[screen])
                )
                UAVs[uav_index][screen].setScaledContents(True)
        except Exception as e:
            self.popup_msg(
                f"Update UAV screen view error: {repr(e)}",
                src_msg="update_uav_screen_view",
                type_msg="error",
            )

    # //-/////////////////////////////////////////////////////////////
    # ? display functions

    def template_information(
        self,
        uav_index,
        connection_status="No information",
        arming_status="No information",
        battery_status="No information",
        gps_status="No information",
        mode_status="No information",
        actuator_status="No information",
        altitude_status=["No information", "No information"],
        position_status=["No information", "No information"],
        **kwargs,
    ) -> QtCore.QCoreApplication.translate:
        """
        Generates a formatted string containing various status information for a UAV.

        Args:
            uav_index (int): The index of the UAV.
            connection_status (str, optional): The connection status of the UAV. Defaults to 'No information'.
            arming_status (str, optional): The arming status of the UAV. Defaults to 'No information'.
            battery_status (str, optional): The battery status of the UAV. Defaults to 'No information'.
            gps_status (str, optional): The GPS status of the UAV. Defaults to 'No information'.
            mode_status (str, optional): The mode status of the UAV. Defaults to 'No information'.
            actuator_status (str, optional): The actuator status of the UAV. Defaults to 'No information'.
            altitude_status (list, optional): A list containing the relative and MSL altitude status of the UAV. Defaults to ['No information', 'No information'].
            position_status (list, optional): A list containing the latitude and longitude position status of the UAV. Defaults to ['No information', 'No information'].
            **kwargs: Additional keyword arguments.

        Returns:
            str: A formatted string containing the UAV status information.
        """
        _translate = QtCore.QCoreApplication.translate
        msg = "\n".join(
            [
                f"\t**UAV {uav_index} Information**:".strip(),
                f"{'- Connection:' : <20}{str(connection_status) : ^10}".strip(),
                f"{'- Arming:': <20}{arming_status : ^10}".strip(),
                f"{'- Battery:': <20}{battery_status : ^10}".strip(),
                f"{'- GPS(FIXED):': <20}{gps_status: ^10}".strip(),
                f"{'- Mode:': <20}{mode_status : ^10}".strip(),
                f"{'- Actuator:': <20}{actuator_status : ^10}".strip(),
                f"{'- Altitude:': <20}".strip(),
                f"{'-----Relative:': <20}{altitude_status[0] : ^10}m".strip(),
                f"{'-----MSL:': <20}{altitude_status[1] : ^10}m".strip(),
                f"{'- Position:': <20}".strip(),
                f"{'-----Latitude:': <20}{position_status[0] : ^10} ".strip(),
                f"{'-----Longitude:': <20}{position_status[1] : ^10}".strip(),
                "================================",
            ]
        )
        return _translate("MainWindow", msg)

    def update_terminal(self, text, uav_index=0) -> None:
        """
        Updates the terminal with the provided text.

        Parameters:
        text (str): The text to append to the terminal.
        uav_index (int, optional): The index of the UAV terminal to update.
                                   Defaults to 0, which updates the main terminal.

        Returns:
        None
        """
        if uav_index == 0:
            self.ui.mainTerminal.setFocus()
            self.ui.mainTerminal.moveCursor(self.ui.mainTerminal.textCursor().End)
            self.ui.mainTerminal.appendPlainText(text)
        else:
            self.uav_status_views[uav_index - 1].setFocus()
            self.uav_status_views[uav_index - 1].moveCursor(
                self.uav_status_views[uav_index - 1].textCursor().End
            )
            self.uav_status_views[uav_index - 1].appendPlainText(text)

    # //-/////////////////////////////////////////////////////////////
    # ? map handling functions

    def onMarkerMoved(self, key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)

    def onMarkerRClick(self, key, latitude, longitude):
        print("RClick on ", key)
        # map.setMarkerOptions(key, draggable=False)

    def onMarkerLClick(self, key, latitude, longitude):
        print("LClick on ", key)

    def onMarkerDClick(self, key, latitude, longitude):
        print("DClick on ", key)
        # map.setMarkerOptions(key, draggable=True)

    def onMapMoved(self, latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(self, latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(self, latitude, longitude):
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude):
        print("DClick on ", latitude, longitude)

    def onPolygonDrawn(self, json):
        print("Polygon Drawn", json)

    # ? handling error functions

    def popup_msg(self, msg, src_msg="", type_msg="error"):
        """Create popup window to the ui

        Args:
            msg(str): message you want to show to the popup window
            src_msg(str, optional): source of the message. Defaults to ''.
            type_msg(str, optional): type of popup. Available: warning, error, information. Defaults to 'error'.
        """
        try:
            self.popup = QMessageBox()
            if type_msg.lower() == "warning":
                self.popup.setIcon(QMessageBox.Warning)
                self.is_error = True
            elif type_msg.lower() == "error":
                self.popup.setIcon(QMessageBox.Critical)
                self.is_error = True
            elif type_msg.lower() == "info":
                self.popup.setIcon(QMessageBox.Information)

            self.popup.setText(
                f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}"
            )
            self.popup.setStandardButtons(QMessageBox.Ok)
            self.popup.exec_()

            print(f"[{type_msg.upper()}]: {repr(msg)} from {src_msg}")

        except Exception as e:
            print("-> From: popup_msg", e)


def run():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = App()

    MainWindow.setWindowIcon(QtGui.QIcon(f"{parent_dir.parent}/assets/icons/app.png"))
    MainWindow.show()

    with loop:
        # # asyncio.all_tasks() Return a set of not yet finished Task objects run by the loop. Based on definition, pending will always be an empty set.
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
    run()
