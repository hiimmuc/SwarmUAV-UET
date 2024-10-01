import asyncio
import os
import sys
from threading import Thread

import cv2
from asyncqt import QEventLoop, asyncSlot
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from ultralytics import YOLO

from config import *
from UI.interface_uav import *
from utils.drone_utils import *
from utils.map_utils import *
from utils.mavsdk_server_utils import *
from utils.model_utils import *
from utils.qt_utils import *

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


# UAVs object
UAVs = {
    uav_index: {
        "server": Server(
            id=uav_index,
            proto=PROTO,
            server_host=SERVER_HOST,
            port=DEFAULT_PORT + uav_index - 1,
            bind_port=DEFAULT_BIND_PORT + uav_index - 1,
        ),
        "system": System(mavsdk_server_address="localhost", port=DEFAULT_PORT + uav_index - 1),
        "system_address": f"{PROTO}://{SERVER_HOST}:{DEFAULT_BIND_PORT + uav_index- 1}",
        "streaming_address": DEFAULT_STREAM_VIDEO_PATHS[uav_index - 1],
        "connection_allow": connection_allows[uav_index - 1],
        "streaming_enable": streaming_enables[uav_index - 1],
    }
    for uav_index in range(1, MAX_UAV_COUNT + 1)
}


class App(QMainWindow):
    def __init__(self, model_path=None) -> None:
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # starting stack and tab index
        self.active_tab_index = 0
        self.active_stack_index = 0

        # UAVs
        self.uav_stream_threads = [None for _ in range(1, MAX_UAV_COUNT + 1)]

        self.uav_stream_captures = [None for _ in range(1, MAX_UAV_COUNT + 1)]

        self.uav_stream_writers = [None for _ in range(1, MAX_UAV_COUNT + 1)]

        # UAVs UI components
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
        print(f"Application initialized at {NOW}")

        self.predictor = YOLO(model_path).to(DEVICE)
        print("Model loaded successfully")

        # ---------------------------------------------------------

    def init_application(self) -> None:
        """
        Initializes the application by setting up the UI components and their default values.

        Tasks include resetting paths, setting images, configuring map views, initializing callbacks,
        and setting default values for UI elements.

        Returns:
            None
        """

        # set logo
        self.ui.page_name.setPixmap(QtGui.QPixmap(logo1_path))
        self.ui.page_name.setScaledContents(True)
        self.ui.page_name_2.setPixmap(QtGui.QPixmap(logo1_path))
        self.ui.page_name_2.setScaledContents(True)
        self.ui.logo2_2.setPixmap(QtGui.QPixmap(logo2_path))
        self.ui.logo2_2.setScaledContents(True)
        self.ui.logo2.setPixmap(QtGui.QPixmap(logo2_path))
        self.ui.logo2.setScaledContents(True)

        # screen view default image
        for screen in self.uav_general_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["general_screen"]))
            screen.setScaledContents(False)
        for screen in self.uav_stream_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["stream_screen"]))
            screen.setScaledContents(False)
        for screen in self.uav_ovv_screen_views:
            screen.setPixmap(QtGui.QPixmap(noSignal_img_paths["ovv_screen"]))
            screen.setScaledContents(False)

        # map URL

        self.ui.MapWebView.setUrl(QtCore.QUrl(map_html_path))

        self.ui.Overview_map_view.setUrl(QtCore.QUrl(map_html_path))

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

        # self.map.markerMovedCallback = self.onMarkerMoved
        # self.map.markerClickedCallback = self.onMarkerLClick
        # self.map.markerDoubleClickedCallback = self.onMarkerDClick
        # self.map.markerRightClickedCallback = self.onMarkerRClick

        self.ovv_map = MapEngine(self.ui.Overview_map_view)
        self.ovv_map.mapMovedCallback = self.onMapMoved
        self.ovv_map.mapClickedCallback = self.onMapLClick
        self.ovv_map.mapDoubleClickedCallback = self.onMapDClick
        self.ovv_map.mapRightClickedCallback = self.onMapRClick

    # ---------------------------<UI Events>---------------------------
    def _uav_to_widgets(self) -> None:
        """
        Maps UAV components to their respective UI elements.

        Iterates over a predefined number of UAVs (MAX_UAV_COUNT) and assigns various UI elements
        and initial status information to each UAV.

        Attributes:
            UAVs (dict): Dictionary with UI elements and status information for each UAV.
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

        self.ui.actionOverview.triggered.connect(lambda: self._switch_layout("main page", "all"))
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
        Maps UI button click events to UAV control functions using async tasks.

        Connects buttons to functions for UAV operations like arming, disarming, opening/closing,
        landing, taking off, pausing missions, connecting, returning, and pushing missions.
        Also maps buttons for setting/getting UAV flight info, updating settings, and navigation.

        Buttons mapped:
        - Arm, Disarm, Open/Close, Landing, Take Off, Pause Mission, Connect, Return, Mission, Push Mission
        - Set/Get Flight Info (for each UAV)
        - Update Settings (for 'settings' and 'overview' pages)
        - Go To (for 'settings' and 'overview' pages)
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
            lambda: asyncio.create_task(self.uav_fn_return(self.active_tab_index, rtl=True))
        )

        self.ui.btn_return.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_return(self.active_tab_index, rtl=False))
        )

        self.ui.btn_mission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_mission(self.active_tab_index))
        )

        self.ui.btn_pushMission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_pushMission(self.active_tab_index))
        )

        self.ui.btn_toggle_camera.clicked.connect(
            lambda: self.uav_fn_toggle_camera(self.active_tab_index)
        )

        for i, btn in enumerate(self.uav_set_param_buttons):
            btn.clicked.connect(
                lambda i=i: asyncio.create_task(self.uav_fn_set_flight_info(i + 1))
            )

        for i, btn in enumerate(self.uav_get_param_buttons):
            btn.clicked.connect(
                lambda i=i: asyncio.create_task(
                    self.uav_fn_get_flight_info(uav_index=i + 1, copy=True)
                )
            )

        # all is update table
        self.ui.btn_sett_cf_nSwarms.clicked.connect(lambda: self._modify_tables(mode="settings"))
        self.ui.btn_ovv_cf_nSwarms.clicked.connect(lambda: self._modify_tables(mode="overview"))

        # go to buttons
        for i, buttons in enumerate(zip(self.uav_sett_goTo_buttons, self.uav_ovv_goTo_buttons)):
            buttons[0].clicked.connect(
                lambda uav_index=i: asyncio.create_task(self.uav_fn_goTo(uav_index, "settings"))
            )
            buttons[1].clicked.connect(
                lambda uav_index=i: asyncio.create_task(self.uav_fn_goTo(uav_index, "overview"))
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
                lambda uav_index=index + 1: asyncio.create_task(self.process_command(uav_index))
            )

    def _create_streaming_threads(self, uav_indexes=None) -> None:
        """
        Connects the `change_image_signal` of each UAV view thread to the `update_uav_screen_view` method.

        This method iterates over a range defined by `MAX_UAV_COUNT` and sets up a connection for each UAV view thread.
        The connection is made such that when the `change_image_signal` is emitted, the `update_uav_screen_view`
        method is called with the corresponding UAV index.

        Args:
            None

        Returns:
            None
        """
        global UAVs
        try:
            if uav_indexes is None:
                uav_indexes = range(1, MAX_UAV_COUNT + 1)
            for uav_index in uav_indexes:
                if not (
                    UAVs[uav_index]["streaming_enable"] and UAVs[uav_index]["connection_allow"]
                ):
                    return

                self.uav_stream_threads[uav_index - 1] = Thread(
                    target=self.stream_on_uav_screen,
                    args=(uav_index,),
                    name=f"UAV-{uav_index}-thread",
                )

                self.uav_stream_captures[uav_index - 1] = cv2.VideoCapture(
                    UAVs[uav_index]["streaming_address"]
                )

                self.uav_stream_writers[uav_index - 1] = cv2.VideoWriter(
                    filename=DEFAULT_STREAM_VIDEO_LOG_PATHS[uav_index - 1],
                    fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
                    fps=20.0,
                    frameSize=DEFAULT_STREAM_SIZE,
                )

                print(f"UAV-{uav_index} streaming thread created.")
        except Exception as e:
            print(f"Error: {repr(e)}")
            self.popup_msg(type_msg="Error", msg=repr(e), src_msg="_create_streaming_threads()")

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

        boxes_checked = []
        for i, widget in enumerate(self.sett_checkBox_active_lists):
            UAVs[i + 1]["connection_allow"] = widget.isChecked()
            if widget.isChecked():
                boxes_checked.append(i + 1)
        return boxes_checked

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
            if mode != "init":  # get the values from the table in runtime
                checked_uav_indexes = self._handling_checkBoxes(mode=mode)
                # get values from the table
                if mode == "settings":
                    nSwarms = min(int(self.ui.nSwarms_sett.value()), len(checked_uav_indexes))
                    dataFrame_widget = get_values_from_table(
                        self.ui.table_uav_large, headers=headers
                    )
                else:
                    nSwarms = min(int(self.ui.nSwarms_ovv.value()), len(checked_uav_indexes))
                    dataFrame_widget = get_values_from_table(
                        self.ui.table_uav_small, headers=headers
                    )

                # get data from address columns
                for i in range(1, MAX_UAV_COUNT + 1):
                    if i in checked_uav_indexes:
                        UAVs[i]["system_address"], port = dataFrame_widget["connection_address"][
                            i - 1
                        ].split("-p")
                        UAVs[i]["system"]._port = int(port)
                        # get streaming address
                        if "VIDEO: " in dataFrame_widget["streaming_address"][i - 1]:
                            UAVs[i]["streaming_address"] = str(
                                dataFrame_widget["streaming_address"][i - 1].replace("VIDEO: ", "")
                            )
                        elif "LOCAL: " in dataFrame_widget["streaming_address"][i - 1]:
                            UAVs[i]["streaming_address"] = int(
                                dataFrame_widget["streaming_address"][i - 1]
                                .replace("LOCAL: ", "")
                                .strip()
                            )
                        else:
                            UAVs[i]["streaming_address"] = str(
                                dataFrame_widget["streaming_address"][i - 1].replace(
                                    "STREAM: ", ""
                                )
                            )

                # update the table
                self._update_tables(
                    data=dataFrame_widget,
                    indexes=checked_uav_indexes,
                    nSwarms=nSwarms,
                    headers=headers,
                )
                print("[INFO] Updated UAVs values according to the table")
                # re-create streaming threads
                self._create_streaming_threads()
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
                indexes = [
                    uav_index
                    for uav_index in range(1, MAX_UAV_COUNT + 1)
                    if UAVs[uav_index]["connection_allow"]
                ]

                self._update_tables(
                    data=data, indexes=indexes, nSwarms=len(indexes), headers=headers
                )

        except Exception as e:
            self.popup_msg(msg=f"Error: {repr(e)}", src_msg="_modify_tables", type_msg="Error")

    def _update_tables(self, data, indexes, nSwarms, headers) -> None:
        """
        Updates the table with the given data and headers.

        Args:
            data (dict): A dictionary containing the data to be displayed in the table.
            indexes (list): A list of indices to display in the table.
            nSwarms (int): The number of swarms to display in the table.
            headers (list): A list of headers for the table.

        Returns:
            None
        """
        if type(data) is not pd.DataFrame:
            data = pd.DataFrame.from_dict(data)

        # 1. update the tables
        draw_table(
            self.ui.table_uav_large,
            data=pd.DataFrame.from_dict(data),
            indexes=indexes[:nSwarms],
            headers=headers,
        )
        draw_table(
            self.ui.table_uav_small,
            data=pd.DataFrame.from_dict(data),
            indexes=indexes[:nSwarms],
            headers=headers,
        )

        # 2. update the nSwarms
        self.ui.nSwarms_sett.setValue(nSwarms)
        self.ui.nSwarms_ovv.setValue(nSwarms)
        pass

    # ////////////////////////////////////////////////////////////////

    async def process_command(self, uav_index) -> None:
        """
        Processes a command for a UAV based on the given index.

        Args:
            uav_index (int): The index of the UAV to process the command for.

        Raises:
            Exception: If the input command is invalid.

        This method retrieves the command text, parses it, and executes the corresponding
        action for the UAV. Supported commands include 'forward', 'backward', 'left',
        'right', 'up', and 'down'. Clears the input field after processing.
        """
        try:
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

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
                    await self.uav_fn_goTo_distance(self.active_tab_index, command, distance)
                    # await UAVs[uav_index]["system"].action.hold()
                # Clear the input after processing the command
                self.uav_update_commands[uav_index - 1].clear()

        except Exception as e:
            self.popup_msg(
                f"Invalid input: {repr(e)}", src_msg="process_command", type_msg="Error"
            )

    # -----------------------< UAV buttons functions >-----------------------
    async def uav_fn_connect(self, uav_index) -> None:
        """
        Asynchronously connects to a UAV or all UAVs.

        Args:
            uav_index (int): The index of the UAV to connect to. If 0, connects to all UAVs.

        Raises:
            Exception: If there is an error during the connection process.
        """
        global UAVs
        try:
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                if not UAVs[uav_index]["connection_allow"]:
                    self.update_terminal(f"[INFO] Connection not allowed for UAV {uav_index}")
                    return

                self.update_terminal(f"[INFO] Sent CONNECT command to UAV {uav_index}")
                # set default information
                self.set_default_uav_information_display(uav_index)
                # init server
                UAVs[uav_index]["server"].start()

                await asyncio.sleep(5)

                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )

                UAVs[uav_index]["uav_information"]["connection_status"] = True

                UAVs[uav_index]["information_view"].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
                )

                await self.uav_fn_check_connection(uav_index)

                # await self.uav_fn_get_status(uav_index)

            else:
                connect_all_UAVs = [self.uav_fn_connect(i) for i in range(1, MAX_UAV_COUNT + 1)]
                await asyncio.gather(*connect_all_UAVs)

        except Exception as e:
            self.set_default_uav_information_display(uav_index)

            self.popup_msg(
                f"Connection error to uav {uav_index} :{repr(e)}",
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
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            self.update_terminal(f"[INFO] Sent ARM command to UAV {uav_index}")
            #
            await UAVs[uav_index]["system"].connect(
                system_address=UAVs[uav_index]["system_address"]
            )
            await UAVs[uav_index]["system"].action.arm()
            await asyncio.sleep(3)
            await self.uav_fn_disarm(uav_index)

            UAVs[uav_index]["uav_information"]["arming_status"] = "ARMED"
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )
        else:
            arm_all_UAVs = [self.uav_fn_arm(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*arm_all_UAVs)

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
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

            self.update_terminal(f"[INFO] Sent DISARM command to UAV {uav_index}")

            await UAVs[uav_index]["system"].action.disarm()

            UAVs[uav_index]["uav_information"]["arming_status"] = "DISARMED"
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

        else:
            disarm_all_UAVs = [self.uav_fn_disarm(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*disarm_all_UAVs)

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
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

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
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

        else:
            takeoff_all_UAVs = [self.uav_fn_takeoff(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*takeoff_all_UAVs)

    async def uav_fn_landing(self, uav_index) -> None:
        """
        Asynchronously commands a UAV or all UAVs to land.

        Args:
            uav_index (int): The index of the UAV to land. If 0, lands all UAVs.

        Returns:
            None
        """
        global UAVs
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

            self.update_terminal(f"[INFO] Sent LANDING command to UAV {uav_index}")

            await UAVs[uav_index]["system"].action.land()

            UAVs[uav_index]["uav_information"]["mode_status"] = "LANDING"
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

        else:
            landing_all_UAVs = [self.uav_fn_landing(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*landing_all_UAVs)

    async def uav_fn_return(self, uav_index, rtl=False) -> None:
        """
        Asynchronously pauses the mission of a UAV or all UAVs.

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
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                if not (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):
                    return
                # if return to launch, which means the UAV will return to the initial position and land
                if rtl:
                    self.update_terminal(f"[INFO] Sent RTL command to UAV {uav_index}")

                    init_longitude = UAVs[uav_index]["uav_information"]["init_longitude"]
                    init_latitude = UAVs[uav_index]["uav_information"]["init_latitude"]
                    current_longitude = UAVs[uav_index]["uav_information"]["position_status"][1]
                    current_latitude = UAVs[uav_index]["uav_information"]["position_status"][0]
                    if (init_longitude == current_longitude) and (
                        init_latitude == current_latitude
                    ):
                        self.update_terminal(
                            f"[INFO] UAV {uav_index} is already at the initial position, landing..."
                        )
                        await UAVs[uav_index]["system"].action.land()
                    else:
                        await UAVs[uav_index]["system"].action.set_return_to_launch_altitude(
                            UAVs[uav_index]["uav_information"]["init_height"]
                        )
                        await UAVs[uav_index]["system"].action.return_to_launch()

                    UAVs[uav_index]["uav_information"]["mode_status"] = "RTL"
                    UAVs[uav_index]["information_view"].setText(
                        self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
                    )
                else:  # return to initial position
                    self.update_terminal(
                        f"[INFO] Sent RETURN command to UAV {uav_index} \
                            to lat: {UAVs[uav_index]['uav_information']['init_latitude']} \
                                long: {UAVs[uav_index]['uav_information']['init_longitude']}"
                    )

                    await self.uav_fn_goTo_location(
                        uav_index,
                        latitude=UAVs[uav_index]["uav_information"]["init_latitude"],
                        longitude=UAVs[uav_index]["uav_information"]["init_longitude"],
                    )

                    UAVs[uav_index]["uav_information"]["mode_status"] = "Return"
                    UAVs[uav_index]["information_view"].setText(
                        self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
                    )
            else:
                return_all_UAVs = [
                    self.uav_fn_return(i, rtl=rtl) for i in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*return_all_UAVs)

        except Exception as e:
            self.popup_msg(f"Return error: {repr(e)}", src_msg="uav_fn_return", type_msg="error")

    async def uav_fn_mission(self, uav_index) -> None:
        """NOTE: convert file points to .plan file as in ./data/mission.plan
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
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                if not (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):
                    return

                self.update_terminal(f"[INFO] Sent MISSION command to UAV {uav_index}")

                # create tasks for monitoring mission progress and observing if the UAV is in the air
                print_mission_progress_task = asyncio.ensure_future(
                    print_mission_progress(UAVs[uav_index]["system"])
                )
                running_tasks = [print_mission_progress_task]
                termination_task = asyncio.ensure_future(
                    observe_is_in_air(UAVs[uav_index]["system"], running_tasks)
                )

                # NOTE: 1. push mission

                mission_items = []
                # Assign hight for mission
                height = UAVs[uav_index]["uav_information"]["init_height"]
                # read mission points from file
                with open(f"{SRC_DIR}/logs/points/points{uav_index}.txt", "r") as file:
                    for line in file:
                        latitude, longitude = map(float, line.strip().split(", "))
                        mission_items.append(
                            MissionItem(
                                latitude_deg=latitude,
                                longitude_deg=longitude,
                                relative_altitude_m=height,
                                speed_m_s=float("nan"),
                                is_fly_through=False,
                                gimbal_pitch_deg=float("nan"),
                                gimbal_yaw_deg=float("nan"),
                                loiter_time_s=10,
                                acceptance_radius_m=float("nan"),
                                yaw_deg=float("nan"),
                                camera_action=MissionItem.CameraAction.NONE,
                                camera_photo_distance_m=float("nan"),
                                camera_photo_interval_s=float("nan"),
                                vehicle_action=MissionItem.VehicleAction.NONE,
                            )
                        )

                mission_plan = MissionPlan(mission_items)

                # set return to launch after mission
                await UAVs[uav_index]["system"].mission.set_return_to_launch_after_mission(True)
                # upload mission
                await UAVs[uav_index]["system"].mission.upload_mission(mission_plan)

                # Health check before mission
                self.update_terminal(
                    "Waiting for drone to have a global position estimate...", uav_index=uav_index
                )
                async for health in UAVs[uav_index]["system"].telemetry.health():
                    if health.is_global_position_ok and health.is_home_position_ok:
                        print("-- Global position estimate OK")
                        break

                # NOTE: 2. Perform mission

                await UAVs[uav_index]["system"].action.arm()
                await UAVs[uav_index]["system"].mission.start_mission()

                UAVs[uav_index]["uav_information"]["mode_status"] = "Mission"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
                )

                # wait for mission to complete
                await termination_task

            else:
                mission_all_UAVs = [self.uav_fn_mission(i) for i in range(1, MAX_UAV_COUNT + 1)]
                await asyncio.gather(*mission_all_UAVs)

        except Exception as e:
            self.popup_msg(f"Mission error: {repr(e)}", src_msg="uav_fn_mission", type_msg="error")

    async def uav_fn_pushMission(self, uav_index) -> None:
        """NOTE: convert file points to .plan file as in ./data/mission.plan
        Pushes a mission to a specified UAV or all UAVs if uav_index is 0.

        Args:
            uav_index (int): The index of the UAV to push the mission to. If 0, pushes to all UAVs.

        Raises:
            Exception: If there is an error during the mission push process.

        Notes:
            - Checks the connection status of the UAV.
            - Reads mission points from a user-selected file.
            - Uploads the mission and sets return to launch after mission.
            - Updates the UAV's mode status to 'Mission pushing'.
        """
        global UAVs
        try:
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                if not (
                    UAVs[uav_index]["uav_information"]["connection_status"]
                    and UAVs[uav_index]["connection_allow"]
                ):
                    return

                self.update_terminal(f"[INFO] Sent PUSH MISSION command to UAV {uav_index}")

                # read mission points from file
                fpath = QFileDialog.getOpenFileName(
                    self,
                    "Open file",
                    plans_log_dir,
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
                        mission_items.append(
                            MissionItem(
                                latitude_deg=latitude,
                                longitude_deg=longitude,
                                relative_altitude_m=height,
                                speed_m_s=float("nan"),
                                is_fly_through=False,
                                gimbal_pitch_deg=float("nan"),
                                gimbal_yaw_deg=float("nan"),
                                loiter_time_s=10,
                                acceptance_radius_m=float("nan"),
                                yaw_deg=float("nan"),
                                camera_action=MissionItem.CameraAction.NONE,
                                camera_photo_distance_m=float("nan"),
                                camera_photo_interval_s=float("nan"),
                                vehicle_action=MissionItem.VehicleAction.NONE,
                            )
                        )
                mission_plan = MissionPlan(mission_items)

                # set return to launch after mission
                await UAVs[uav_index]["system"].mission.set_return_to_launch_after_mission(True)
                # upload mission
                await UAVs[uav_index]["system"].mission.upload_mission(mission_plan)
                #
                UAVs[uav_index]["uav_information"]["mode_status"] = "Mission pushing"
                UAVs[uav_index]["information_view"].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
                )
            else:
                self.popup_msg(
                    msg="Buttons are disabled on this tab",
                    type_msg="warning",
                    src_msg="uav_fn_pushMission",
                )
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
        """
        global UAVs
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

            self.update_terminal(f"[INFO] Sent PAUSE command to UAV {uav_index}")

            await UAVs[uav_index]["system"].mission.pause_mission()
            #
            UAVs[uav_index]["uav_information"]["mode_status"] = "Mission paused"
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

        else:
            pauseMission_all_UAVs = [
                self.uav_fn_pauseMission(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*pauseMission_all_UAVs)

    async def uav_fn_openClose(self, uav_index) -> None:
        """
        Asynchronously toggles the actuator status of a specified UAV or all UAVs.

        Args:
            uav_index (int): The index of the UAV to toggle. If 0, toggles all UAVs.

        Returns:
            None
        """
        global UAVs
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["uav_information"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

            self.update_terminal(f"[INFO] Sent OPEN/CLOSE command to UAV {uav_index}")

            if UAVs[uav_index]["uav_information"]["actuator_status"]:
                await UAVs[uav_index]["system"].action.set_actuator(uav_index, 0)
                UAVs[uav_index]["uav_information"]["actuator_status"] = False
            else:
                await UAVs[uav_index]["system"].action.set_actuator(uav_index, 1)
                UAVs[uav_index]["uav_information"]["actuator_status"] = True

            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

        else:
            openClose_all_UAVs = [self.uav_fn_openClose(i) for i in range(1, MAX_UAV_COUNT + 1)]
            await asyncio.gather(*openClose_all_UAVs)

    def uav_fn_toggle_camera(self, uav_index) -> None:
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
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                if not (
                    UAVs[uav_index]["connection_allow"] and UAVs[uav_index]["streaming_enable"]
                ):
                    return

                if not UAVs[uav_index]["uav_information"]["streaming_status"]:
                    if not self.uav_stream_threads[uav_index - 1].is_alive():
                        self._create_streaming_threads(uav_indexes=[uav_index])
                        self.uav_stream_threads[uav_index - 1].start()

                    UAVs[uav_index]["uav_information"]["streaming_status"] = True
                    print(f"UAV-{uav_index} streaming thread started.")
                else:
                    # self.uav_stream_threads[uav_index - 1].terminate()
                    UAVs[uav_index]["uav_information"]["streaming_status"] = False
                    print(f"UAV-{uav_index} streaming thread stopped.")
            else:
                for uav_index in range(1, MAX_UAV_COUNT + 1):
                    self.uav_fn_toggle_camera(uav_index)
        except Exception as e:
            print(f"Error: {repr(e)}")
            self.popup_msg(type_msg="Error", msg=repr(e), src_msg="uav_fn_toggle_camera")

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
        try:
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

            if uav_index in range(1, MAX_UAV_COUNT + 1):
                await self.uav_fn_goTo_location(uav_index, latitude=latitude, longitude=longitude)
            else:
                goTo_all_UAVs = [
                    self.uav_fn_goTo_location(i, latitude=latitude, longitude=longitude)
                    for i in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*goTo_all_UAVs)
        except Exception as e:
            self.popup_msg(f"Go to error: {repr(e)}", src_msg="uav_fn_goTo", type_msg="error")

    # -----------------------------< UAVs utility functions >-----------------------------

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
            else:
                self.popup_msg(
                    "Invalid direction", src_msg="uav_fn_goTo_distance", type_msg="info"
                )
            # go to the new position
            await self.uav_fn_goTo_location(uav_index, lat, lon, alt)
            break
        return

    async def uav_fn_goTo_location(
        self, uav_index, latitude, longitude, height=None, *args
    ) -> None:
        """
        Asynchronously commands a UAV to go to a specified geographic point.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.
            latitude (float): The latitude of the target location.
            longitude (float): The longitude of the target location.
            *args: Additional arguments (not used).

        Returns:
            None

        Notes:
            - Retrieves the current altitude and commands the UAV to go to the specified location.
            - Does nothing if the UAV's connection status is inactive.
        """
        global UAVs
        if not height:
            height = UAVs[uav_index]["uav_information"]["init_height"]
        await UAVs[uav_index]["system"].action.goto_location(latitude, longitude, height, 0)

    async def uav_fn_goTo_UAVs(self, uav_indexes, *args) -> None:
        """NOTE: Not used
        Asynchronously directs a UAV to a specified location based on coordinates read from a file.

        Args:
            uav_index (int): The index of the UAV in the UAVs list.
            *args: Additional arguments (not used in this function).

        Returns:
            None

        Behavior:
            - Checks if the UAV at the given index has an active connection.
            - Reads target latitude and longitude from a file located at '{SRC_DIR}/logs/detect/detect.txt'.
            - Continuously checks the UAV's current position.
            - Commands the UAV to move to the target location if it is not already there.
            - Logs a message when the UAV reaches the target location.
        """
        global UAVs
        if len(uav_indexes) == 1:
            uav_index = uav_indexes[0]
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                folder_path = f"{SRC_DIR}/logs/detect"
                txt_file_path = os.path.join(folder_path, "detect.txt")
                with open(txt_file_path, "r") as file:
                    content = file.read()
                    lat_detect, lon_detect = map(float, content.strip().split(", "))

                async for position in UAVs[uav_index]["system"].telemetry.position():
                    if (
                        abs(position.latitude_deg - lat_detect) < 0.00001
                        and abs(position.longitude_deg - lon_detect) < 0.00001
                    ):
                        self.update_terminal(f"[INFO] UAV {uav_index} is at the target location")
                        break
                    height = position.absolute_altitude_m
                    await self.uav_fn_goTo_location(uav_index, lat_detect, lon_detect, height)
            elif uav_index == 0:
                goto_all_UAVs = [self.uav_fn_goTo_UAV(i) for i in range(1, MAX_UAV_COUNT + 1)]
                await asyncio.gather(*goto_all_UAVs)
        else:
            await asyncio.gather(*[self.uav_fn_goTo_UAV(uav_index) for uav_index in uav_indexes])

    # --------------------------<UAVs get status functions>-----------------------------
    async def uav_fn_get_altitude(self, uav_index) -> None:
        """
        Retrieves and updates the altitude and position of a specified UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None

        Notes:
            - Checks if the UAV is connected.
            - Retrieves telemetry data (relative altitude, absolute altitude, latitude, longitude).
            - Updates the UAV's information and writes GPS data to a log file.
        """
        global UAVs
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
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )
            with open(gps_log_paths[uav_index - 1], "w") as f:
                f.write(str(latitude) + ", " + str(longitude))

    async def uav_fn_get_mode(self, uav_index) -> None:
        """
        Retrieves and updates the flight mode status of a UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None
        """
        global UAVs
        async for mode in UAVs[uav_index]["system"].telemetry.flight_mode():
            mode_status = mode
            UAVs[uav_index]["uav_information"]["mode_status"] = mode_status
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

    async def uav_fn_get_battery(self, uav_index) -> None:
        """
        Retrieves and updates the battery status of a UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None
        """
        global UAVs
        async for battery in UAVs[uav_index]["system"].telemetry.battery():
            battery_status = round(battery.remaining_percent * 100, 1)
            UAVs[uav_index]["uav_information"]["battery_status"] = str(battery_status) + "%"
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

    async def uav_fn_get_arm_status(self, uav_index) -> None:
        """
        Retrieves and updates the arming status of a UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None
        """
        global UAVs
        async for arm_status in UAVs[uav_index]["system"].telemetry.armed():
            arm_status = "ARMED" if arm_status else "DISARMED"
            UAVs[uav_index]["uav_information"]["arming_status"] = arm_status
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

    async def uav_fn_get_gps(self, uav_index) -> None:
        """
        Retrieves and updates GPS information for a specified UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None
        """
        global UAVs
        async for gps in UAVs[uav_index]["system"].telemetry.gps_info():
            gps_status = gps.fix_type
            UAVs[uav_index]["uav_information"]["gps_status"] = gps_status
            UAVs[uav_index]["information_view"].setText(
                self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
            )

    async def uav_fn_get_flight_info(self, uav_index, copy=False) -> None:
        """
        Retrieves and updates flight parameters for a specified UAV.

        Args:
            uav_index (int): The index of the UAV.
            copy (bool, optional): If True, copies parameters to another set of display fields. Defaults to False.

        Notes:
            - Retrieves parameters like takeoff altitude, disarm land command, and speeds.
            - Displays a warning if the UAV is not connected.
        """
        global UAVs
        try:
            parameters = {}
            parameters["MIS_TAKEOFF_ALT"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MIS_TAKEOFF_ALT"
            )
            parameters["COM_DISARM_LAND"] = await UAVs[uav_index]["system"].param.get_param_float(
                "COM_DISARM_LAND"
            )
            parameters["MPC_TKO_SPEED"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MPC_TKO_SPEED"
            )
            parameters["MPC_LAND_SPEED"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MPC_LAND_SPEED"
            )
            parameters["MPC_XY_P"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MPC_XY_P"
            )
            parameters["MPC_XY_VEL_D_ACC"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MPC_XY_VEL_D_ACC"
            )
            parameters["MPC_XY_VEL_P_ACC"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MPC_XY_VEL_P_ACC"
            )
            parameters["MC_PITCH_P"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MC_PITCH_P"
            )
            parameters["MC_ROLL_P"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MC_ROLL_P"
            )
            parameters["MC_YAW_P"] = await UAVs[uav_index]["system"].param.get_param_float(
                "MC_YAW_P"
            )
            # update display fields
            for i, (_, value) in enumerate(parameters.items()):
                UAVs[uav_index]["param_display"].children()[i + 1].setText(str(round(value, 1)))

            if copy:  # copy parameters from display fields to set fields
                for i, (_, value) in enumerate(parameters.items()):
                    UAVs[uav_index]["param_set"].children()[i + 1].setText(str(round(value, 1)))

        except Exception as e:
            self.popup_msg(
                f"Get flight info error: {repr(e)}",
                src_msg="uav_fn_get_flight_info",
                type_msg="error",
            )

    async def uav_fn_set_flight_info(self, uav_index) -> None:
        """
        Asynchronously sets flight parameters for a specified UAV.

        Args:
            uav_index (int): The index of the UAV.

        Returns:
            None

        Notes:
            - Retrieves new parameter values and updates the UAV's system.
            - Uses existing values if new ones are not provided.
            - Requires the UAV to be connected.
        """
        global UAVs
        try:
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

        except Exception as e:
            self.popup_msg(
                f"Set flight info error: {repr(e)}",
                src_msg="uav_fn_set_flight_info",
                type_msg="error",
            )

    async def uav_fn_check_connection(self, uav_index) -> None:
        """
        Asynchronously checks the connection status of a UAV and performs setup tasks.

        Args:
            uav_index (int): The index of the UAV to check.

        Returns:
            None

        Steps:
        1. Waits for the UAV to connect and updates the terminal and UI.
        2. Checks if the global position estimate is good for flying.
        3. Sets the maximum speed, retrieves parameters, and writes them to a log file.
        4. Gathers telemetry data like altitude, mode, battery, arm status, GPS, and flight info.

        Note:
            Assumes the UAVs dictionary and update_terminal method are defined elsewhere.
        """
        global UAVs
        print(f"Waiting for drone {uav_index} to connect...")
        async for state in UAVs[uav_index]["system"].core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone {uav_index}!")
                self.update_terminal(f"[INFO] Received CONNECT signal from UAV {uav_index}")
                UAVs[uav_index]["label_param"].setStyleSheet("background-color: green")
                self.sett_checkBox_active_lists[uav_index - 1].setChecked(True)
                set_row_color(self.ui.table_uav_large, uav_index - 1, QtGui.QColor(144, 238, 144))
                set_row_color(self.ui.table_uav_small, uav_index - 1, QtGui.QColor(144, 238, 144))
            break

        # Checking if Global Position Estimate is ok
        async for health in UAVs[uav_index]["system"].telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position state is good enough for flying.")
                break
        #
        if not (
            UAVs[uav_index]["uav_information"]["connection_status"]
            and UAVs[uav_index]["connection_allow"]
        ):
            return

        await UAVs[uav_index]["system"].action.set_maximum_speed(1.0)

        # Get the list of parameters
        # all_params = await UAVs[uav_index]["system"].param.get_all_params()

        # with open(f"{SRC_DIR}/logs/params/params{uav_index}.txt", "w") as f:

        #     for param in all_params.int_params:
        #         f.write(f"{param.name}: {param.value}\n")

        #     for param in all_params.float_params:
        #         f.write(f"{param.name}: {param.value}\n")

        await self.uav_fn_get_status(uav_index)

    async def uav_fn_get_status(self, uav_index) -> None:
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            await asyncio.gather(
                self.uav_fn_printStatus(uav_index),
                self.uav_fn_get_altitude(uav_index),
                self.uav_fn_get_mode(uav_index),
                self.uav_fn_get_battery(uav_index),
                self.uav_fn_get_arm_status(uav_index),
                self.uav_fn_get_gps(uav_index),
                self.uav_fn_get_flight_info(uav_index, copy=False),
            )
        elif uav_index == 0:
            await asyncio.gather(*[self.uav_fn_get_status(i) for i in range(1, MAX_UAV_COUNT + 1)])
        else:
            pass

    async def uav_fn_printStatus(self, uav_index) -> None:
        """
        Asynchronously prints the status of a UAV to the terminal.

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
        """NOTE: This function is not used now, modify later if needed.
        Compares the distance of multiple UAVs to a detected location and directs the closest ones to move.

        Args:
            num_UAVs (int): The number of UAVs to compare and control.
            *args: Additional arguments (not used).

        Returns:
            None

        Reads the detected location from a file, retrieves UAV positions, calculates distances, sorts UAVs by distance, and directs the closest ones to move.
        """
        global UAVs
        if num_UAVs <= 0:
            return

        folder_path = f"{SRC_DIR}/logs/detect"
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
        await self.uav_fn_goTo_UAVs(UAVs_to_control)

    # -----------------------------< UAVs streaming functions >-----------------------------

    def stream_on_uav_screen(self, uav_index, **kwargs) -> None:
        """
        Updates the UAV screen view with the specified UAV's information.

        Args:
            uav_index (int): The index of the UAV to update the screen view for.

        Returns:
            None
        """
        try:
            global UAVs
            # change to connection states later UAVs[uav_index]["uav_information"]["connection_status"]
            if not (UAVs[uav_index]["connection_allow"] and UAVs[uav_index]["streaming_enable"]):
                return

            is_opened = self.uav_stream_captures[uav_index - 1].isOpened()

            while is_opened:
                ret, frame = self.uav_stream_captures[uav_index - 1].read()

                if ret:
                    # detect objects in the frame
                    results = self.predictor(frame, device=DEVICE, stream=True, verbose=False)
                    frame = draw_frame(frame, results)

                    self.update_uav_screen_view(
                        uav_index, frame, screen_name=DEFAULT_STREAM_SCREEN
                    )

                    self.uav_stream_writers[uav_index - 1].write(frame)
                else:
                    self.uav_stream_captures[uav_index - 1].set(cv2.CAP_PROP_POS_FRAMES, 0)

                if not UAVs[uav_index]["uav_information"]["streaming_status"]:
                    break

            self.uav_stream_captures[uav_index - 1].release()
            self.uav_stream_writers[uav_index - 1].release()

            # reset the screen to the pause screen
            pause_frame = cv2.imread(pause_img_paths[DEFAULT_STREAM_SCREEN])
            self.update_uav_screen_view(uav_index, pause_frame, screen_name=DEFAULT_STREAM_SCREEN)

        except Exception as e:
            self.popup_msg(
                f"Stream on UAV screen error: {repr(e)}",
                src_msg="stream_on_uav_screen",
                type_msg="error",
            )

    def update_uav_screen_view(self, uav_index, frame, screen_name="all") -> None:
        """
        Starts streaming video from the specified UAV to the screen view.

        Args:
            uav_index (int): The index of the UAV to start streaming video from.

        Returns:
            None
        """
        try:
            global UAVs
            if screen_name == "all":
                for screen in screen_sizes.keys():
                    UAVs[uav_index][screen].setPixmap(
                        convert_cv2qt(frame, size=screen_sizes[screen])
                    )

            else:
                UAVs[uav_index][screen_name].setPixmap(
                    convert_cv2qt(frame, size=screen_sizes[screen_name])
                )

        except Exception as e:
            print(f"Error in update_uav_screen_view: {repr(e)}")

    # -----------------------------< UI display utility functions >-----------------------------

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
        elif uav_index in range(1, MAX_UAV_COUNT + 1):
            self.uav_status_views[uav_index - 1].setFocus()
            self.uav_status_views[uav_index - 1].moveCursor(
                self.uav_status_views[uav_index - 1].textCursor().End
            )
            self.uav_status_views[uav_index - 1].appendPlainText(text)

    def set_default_uav_information_display(self, uav_index) -> None:
        """
        Sets the default UAV information display for a specified UAV.

        Args:
            uav_index (int): The index of the UAV to set the default information display for.

        Returns:
            None
        """
        global UAVs
        # default is not connected
        UAVs[uav_index]["uav_information"]["connection_status"] = False
        UAVs[uav_index]["label_param"].setStyleSheet("background-color: red")
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
        UAVs[uav_index]["information_view"].setText(
            self.template_information(uav_index, **UAVs[uav_index]["uav_information"])
        )

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

            elif type_msg.lower() == "error":
                self.popup.setIcon(QMessageBox.Critical)

            elif type_msg.lower() == "info":
                self.popup.setIcon(QMessageBox.Information)

            self.popup.setText(f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}")
            self.popup.setStandardButtons(QMessageBox.Ok)
            self.popup.exec_()

            print(f"[{type_msg.upper()}]: {repr(msg)} from {src_msg}")

        except Exception as e:
            print("-> From: popup_msg", e)

    # -----------------------------< Map widget utility functions >-----------------------------

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


# -----------------------------< Main Application Class >-----------------------------
def run():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = App(model_path=model_path)
    MainWindow.setWindowIcon(QtGui.QIcon(app_icon_path))
    MainWindow.show()

    with loop:
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
