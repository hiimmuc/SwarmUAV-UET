import asyncio
import glob
import os
import sys

import cv2
import pyfiglet
from asyncqt import QEventLoop

# mavsdk
from mavsdk import System

# PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

# ultralytics
from ultralytics import YOLO

# user-defined configuration
from config.interface_config import *
from config.stream_config import *
from config.uav_config import *

# user-defined interface
from interface_base import *
from interface_map import *

# user-defined utils
from utils.drone_utils import *
from utils.mavsdk_server_utils import *
from utils.qt_utils import *
from utils.serial_utils import *
from utils.stream_utils import *

# cspell: ignore UAVs mavsdk asyncqt figlet ndarray offboard pixmap qgroundcontrol rtcm imwrite dsize fourcc imread
__version__ = "3.11.0"
__current_time__ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
__current_path__ = os.path.dirname(os.path.abspath(__file__))
__system_info__ = get_system_information()
print("*" * 50 + "\n" + "*" * 50)
print("SYSTEM INFO:\n" + __system_info__)
print("APP VERSION:", __version__, "\nWorking directory:", __current_path__, "\n", "*" * 50)
print(pyfiglet.figlet_format("UAV SWARM CONTROL APP"))
print("*" * 50)
print("CURRENT TIME:", __current_time__)

# UAVs object
try:
    UAVs = {
        uav_index: {
            "ID": uav_index,
            "server": {
                "shell": Server(
                    id=uav_index,
                    proto=PROTOCOLS[uav_index - 1],
                    server_host=SERVER_HOSTS[uav_index - 1],
                    port=CLIENT_PORTS[uav_index - 1],
                    bind_port=SERVER_PORTS[uav_index - 1],
                ),
                "start": False,
            },
            "system": System(mavsdk_server_address="localhost", port=CLIENT_PORTS[uav_index - 1]),
            "system_address": SYSTEMS_ADDRESSES[uav_index - 1],
            "streaming_address": DEFAULT_STREAM_VIDEO_PATHS[uav_index - 1],
            "connection_allow": connection_allows[uav_index - 1],
            "streaming_enable": streaming_enables[uav_index - 1],
            "detection_enable": detection_enables[uav_index - 1],
            "recording_enable": recording_enables[uav_index - 1],
            "init_params": {
                "longitude": INIT_LON,
                "latitude": INIT_LAT,
                "altitude": INIT_ALT[uav_index - 1],
            },
            "status": {
                "connection_status": False,
                "streaming_status": False,
                "on_mission": False,
                "arming_status": "No information",
                "battery_status": "No information",
                "gps_status": "No information",
                "mode_status": "No information",
                "actuator_status": "No information",
                "altitude_status": ["No information", "No information"],
                "position_status": ["No information", "No information"],
            },
            "rescue_first_time": False,
        }
        for uav_index in range(1, MAX_UAV_COUNT + 1)
    }
except Exception as e:
    print(f"[Error]: {repr(e)}")
    sys.exit(1)

logger.log(f"Application initializing...", level="info")


class App(Map, StreamQtThread, Interface, QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        # UAVs
        self.uav_stream_threads = [None for _ in range(1, MAX_UAV_COUNT + 1)]
        self.uav_stream_frame_cnt = [0 for _ in range(1, MAX_UAV_COUNT + 1)]
        logger.log(f"Initialize detection model on {DEVICE}...", level="info")
        #
        start_time = time.time()
        self.uav_detection_models = [
            YOLO(model_uav_paths[uav_index]) for uav_index in range(1, MAX_UAV_COUNT + 1)
        ]
        logger.log(
            f"Detection models loaded successfully in {(time.time() - start_time):3f}s!",
            level="info",
        )
        #
        self.init_application()
        logger.log("Application initialized successfully", level="info")

        # ---------------------------------------------------------

    def init_application(self) -> None:
        """
        Initializes the application by setting up the UI components and their default values.

        Tasks include resetting paths, setting images, configuring map views, initializing callbacks,
        and setting default values for UI elements.

        Returns:
            None
        """
        # set default views
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.tabWidget.setCurrentIndex(0)

        # set buttons click events
        self._button_clicked_event()

        # set line edit event
        self._line_edit_event()

        # set emit signal
        self._create_streaming_threads()

        # handling settings
        self._handling_settings()

    # ---------------------------<UI Events>---------------------------
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
            lambda: asyncio.create_task(self.uav_arm_callback(self.active_tab_index))
        )

        self.ui.btn_disarm.clicked.connect(
            lambda: asyncio.create_task(self.uav_disarm_callback(self.active_tab_index))
        )

        self.ui.btn_open_close.clicked.connect(
            lambda: asyncio.create_task(self.uav_toggle_open_callback(self.active_tab_index))
        )

        self.ui.btn_landing.clicked.connect(
            lambda: asyncio.create_task(self.uav_land_callback(self.active_tab_index))
        )

        self.ui.btn_take_off.clicked.connect(
            lambda: asyncio.create_task(self.uav_takeoff_callback(self.active_tab_index))
        )

        self.ui.btn_pause_resume.clicked.connect(
            lambda: asyncio.create_task(
                self.uav_toggle_pause_mission_callback(self.active_tab_index)
            )
        )

        self.ui.btn_connect.clicked.connect(
            lambda: asyncio.create_task(self.uav_connect_callback(self.active_tab_index))
        )

        self.ui.btn_rtl.clicked.connect(
            lambda: asyncio.create_task(self.uav_return_callback(self.active_tab_index, rtl=True))
        )

        self.ui.btn_return.clicked.connect(
            lambda: asyncio.create_task(self.uav_return_callback(self.active_tab_index, rtl=False))
        )

        self.ui.btn_mission.clicked.connect(
            lambda: asyncio.create_task(self.uav_mission_callback(self.active_tab_index))
        )

        self.ui.btn_push_mission.clicked.connect(
            lambda: asyncio.create_task(self.uav_push_mission_callback(self.active_tab_index))
        )

        self.ui.btn_toggle_camera.clicked.connect(
            lambda: self.uav_toggle_camera_callback(self.active_tab_index)
        )
        # set/get flight info NOTE: uav_index = 1, 2, 3, 4, 5, 6 need to shorten

        self.uav_set_param_buttons[0].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(1))
        )
        self.uav_set_param_buttons[1].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(2))
        )
        self.uav_set_param_buttons[2].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(3))
        )
        self.uav_set_param_buttons[3].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(4))
        )
        self.uav_set_param_buttons[4].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(5))
        )
        self.uav_set_param_buttons[5].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_set_flight_info(6))
        )

        self.uav_get_param_buttons[0].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(1, True))
        )
        self.uav_get_param_buttons[1].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(2, True))
        )
        self.uav_get_param_buttons[2].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(3, True))
        )
        self.uav_get_param_buttons[3].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(4, True))
        )
        self.uav_get_param_buttons[4].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(5, True))
        )
        self.uav_get_param_buttons[5].clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_get_flight_info(6, True))
        )

        # all is update table
        self.ui.btn_sett_cf_nSwarms.clicked.connect(
            lambda: self._handling_settings(mode="settings")
        )
        self.ui.btn_ovv_cf_nSwarms.clicked.connect(
            lambda: self._handling_settings(mode="overview")
        )

        # go to buttons NOTE: uav_index = 0, 1, 2, 3, 4, 5, 6 need to shorten

        self.uav_sett_goTo_buttons[0].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=0, page="settings"))
        )
        self.uav_ovv_goTo_buttons[0].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=0, page="overview"))
        )
        self.uav_sett_goTo_buttons[1].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=1, page="settings"))
        )
        self.uav_ovv_goTo_buttons[1].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=1, page="overview"))
        )
        self.uav_sett_goTo_buttons[2].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=2, page="settings"))
        )
        self.uav_ovv_goTo_buttons[2].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=2, page="overview"))
        )
        self.uav_sett_goTo_buttons[3].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=3, page="settings"))
        )
        self.uav_ovv_goTo_buttons[3].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=3, page="overview"))
        )
        self.uav_sett_goTo_buttons[4].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=4, page="settings"))
        )
        self.uav_ovv_goTo_buttons[4].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=4, page="overview"))
        )
        self.uav_sett_goTo_buttons[5].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=5, page="settings"))
        )
        self.uav_ovv_goTo_buttons[5].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=5, page="overview"))
        )
        self.uav_sett_goTo_buttons[6].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=6, page="settings"))
        )
        self.uav_ovv_goTo_buttons[6].clicked.connect(
            lambda: asyncio.create_task(self.uav_goto_callback(uav_index=6, page="overview"))
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
            uav_indexes = range(1, MAX_UAV_COUNT + 1) if uav_indexes is None else uav_indexes

            for uav_index in uav_indexes:
                if not (
                    (
                        UAVs[uav_index]["connection_allow"]
                        or UAVs[uav_index]["status"]["connection_status"]
                    )
                    and UAVs[uav_index]["streaming_enable"]
                ):
                    continue

                capture = {
                    "index": uav_index,
                    "address": UAVs[uav_index]["streaming_address"],
                    "width": DEFAULT_STREAM_SIZE[0],
                    "height": DEFAULT_STREAM_SIZE[1],
                    "fps": DEFAULT_STREAM_FPS,
                }

                writer = {
                    "index": uav_index,
                    "enable": UAVs[uav_index]["recording_enable"],
                    "filename": DEFAULT_STREAM_VIDEO_LOG_PATHS[uav_index - 1],
                    "fourcc": FOURCC,
                    "frameSize": DEFAULT_STREAM_SIZE,
                }

                stream_config = {
                    "capture": capture,
                    "writer": writer,
                }

                detection_model = (
                    self.uav_detection_models[uav_index - 1]
                    if UAVs[uav_index]["detection_enable"]
                    else None
                )

                self.uav_stream_threads[uav_index - 1] = StreamQtThread(
                    uav_index=uav_index,
                    stream_config=stream_config,
                    detection_model=detection_model,
                )

                logger.log(
                    f"UAV-{uav_index} stream started: \n\
                        -- Capture stream from {os.path.relpath(UAVs[uav_index]['streaming_address'], __current_path__)} \n\
                        -- Save recording to {os.path.relpath(DEFAULT_STREAM_VIDEO_LOG_PATHS[uav_index - 1], __current_path__) if UAVs[uav_index]['recording_enable'] else 'None'}",
                    level="info",
                )

                try:
                    self.uav_stream_threads[uav_index - 1].change_image_signal.disconnect()
                except Exception as e:
                    pass

                self.uav_stream_threads[uav_index - 1].change_image_signal.connect(
                    self.stream_on_uav_screen,
                    Qt.QueuedConnection,
                )

                logger.log(f"UAV-{uav_index} streaming thread created!", level="info")

        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(type_msg="Error", msg=repr(e), src_msg="_create_streaming_threads()")

    # //-/////////////////////////////////////////////////////////////

    def _handling_settings(self, mode="init") -> None:
        # init checkboxes
        self._handling_checkBoxes(mode=mode)
        # init tables
        self._handling_tables(mode=mode)

    def _handling_checkBoxes(self, mode="init") -> None:
        """
        Handle the state of checkboxes and update UAV detection settings.

        Args:
            mode (str): The page context ('init', 'settings' or 'overview').

        Returns:
            list: A list of indices of checked checkboxes.
        """
        global UAVs
        if mode == "init":
            # set default UI values based on the configuration
            for i, widget in enumerate(self.sett_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["detection_enable"])
            for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["detection_enable"])
            for i, widget in enumerate(self.sett_checkBox_active_lists):
                widget.setChecked(UAVs[i + 1]["streaming_enable"])

        elif mode == "settings":
            # get the values from the table in setting page
            for i, widget in enumerate(self.sett_checkBox_detect_lists):
                UAVs[i + 1]["detection_enable"] = widget.isChecked()
            # sync the values to the overview page
            for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["detection_enable"])
            # sync the values to the setting page
            for i, widget in enumerate(self.sett_checkBox_active_lists):
                UAVs[i + 1]["streaming_enable"] = bool(widget.isChecked())
        elif mode == "overview":
            # get the values from the table in overview page
            for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                UAVs[i + 1]["detection_enable"] = widget.isChecked()
            # sync the values to the setting page
            for i, widget in enumerate(self.sett_checkBox_detect_lists):
                widget.setChecked(UAVs[i + 1]["detection_enable"])

    def _handling_tables(self, mode="init") -> None:
        """
        Update settings based on the checked checkboxes and table values.

        Args:
            mode (str): The page context ('init', 'settings' or 'overview').

        Returns:
            None
        """
        global UAVs
        try:
            headers = ["id", "connection_address", "streaming_address"]
            connection_allow_indexes = [
                index + 1 for index in range(MAX_UAV_COUNT) if UAVs[index + 1]["connection_allow"]
            ]
            streaming_enabled_indexes = [
                index + 1 for index in range(MAX_UAV_COUNT) if UAVs[index + 1]["streaming_enable"]
            ]

            if mode != "init":  # get the values from the table in runtime
                # get values from the table
                if mode == "settings":
                    nSwarms = min(int(self.ui.nSwarms_sett.value()), len(connection_allow_indexes))
                    data = get_values_from_table(self.ui.table_uav_large, headers=headers)
                else:
                    nSwarms = min(int(self.ui.nSwarms_ovv.value()), len(connection_allow_indexes))
                    data = get_values_from_table(self.ui.table_uav_small, headers=headers)

                # update data from address columns to UAVs
                for index in range(MAX_UAV_COUNT):
                    uav_index = index + 1
                    if uav_index in connection_allow_indexes:
                        address, client_port = data["connection_address"][index].split("-p")
                        proto, server_host, bind_port = address.split(":")
                        UAVs[uav_index]["server"]["shell"] = Server(
                            id=uav_index,
                            proto=proto,
                            server_host=server_host.replace("//", ""),
                            port=int(client_port),
                            bind_port=int(bind_port),
                        )
                        UAVs[uav_index]["system_address"] = f"{proto}:{server_host}:{bind_port}"
                        UAVs[uav_index]["system"]._port = int(client_port)
                        UAVs[uav_index]["streaming_address"] = data["streaming_address"][
                            index
                        ].strip()

                logger.log("Updated UAVs configuration", level="info")
                # NOTE: re-create streaming threads
                for uav_index in range(1, MAX_UAV_COUNT + 1):
                    UAVs[uav_index]["status"][
                        "connection_status"
                    ] = False  # reset connection status, need to re-open the terminal
                    UAVs[uav_index]["status"]["streaming_status"] = False  # reset

                self._create_streaming_threads()

            else:
                data = {
                    headers[0]: [uav_index for uav_index in range(1, MAX_UAV_COUNT + 1)],
                    headers[1]: [
                        f"{UAVs[uav_index]['system_address']} -p {UAVs[uav_index]['system']._port}"
                        for uav_index in range(1, MAX_UAV_COUNT + 1)
                    ],
                    headers[2]: [
                        f"{UAVs[uav_index]['streaming_address']}"
                        for uav_index in range(1, MAX_UAV_COUNT + 1)
                    ],
                }
                nSwarms = len(connection_allow_indexes)

            self._update_tables(
                data=data,
                connection_allow_indexes=connection_allow_indexes,
                streaming_enabled_indexes=streaming_enabled_indexes,
                nSwarms=nSwarms,
                headers=headers,
            )

        except Exception as e:
            self.popup_msg(msg=f"Error: {repr(e)}", src_msg="_handling_tables", type_msg="Error")

    def _update_tables(
        self, data, connection_allow_indexes, streaming_enabled_indexes, nSwarms, headers
    ) -> None:
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
            connection_allow_indexes=connection_allow_indexes[:nSwarms],
            streaming_enabled_indexes=streaming_enabled_indexes,
            headers=headers,
        )
        draw_table(
            self.ui.table_uav_small,
            data=pd.DataFrame.from_dict(data),
            connection_allow_indexes=connection_allow_indexes[:nSwarms],
            streaming_enabled_indexes=streaming_enabled_indexes,
            headers=headers,
        )

        # 2. update the nSwarms
        self.ui.nSwarms_sett.setValue(nSwarms)
        self.ui.nSwarms_ovv.setValue(nSwarms)

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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return

            text = self.uav_update_commands[uav_index - 1].text()

            if text.lower().strip() == "hold":
                await UAVs[uav_index]["system"].action.hold()
            else:
                command, value = str(text).split("=")
                command = command.strip().lower()
                value = value.strip().lower()

                # NOTE: if command <do something more here>

                # * 1. control movement command
                if command in ["forward", "backward", "left", "right", "up", "down"]:
                    distance = float(value)
                    await uav_fn_goto_distance(
                        drone=UAVs[self.active_tab_index],
                        distance=distance,
                        direction=command,
                    )

                # * 2. control gimbal command
                if command in ["pitch", "yaw"]:
                    angle = float(value)
                    control_value = (
                        {"pitch": angle, "yaw": 0}
                        if command == "pitch"
                        else {"pitch": 0, "yaw": angle}
                    )
                    await uav_fn_control_gimbal(
                        drone=UAVs[self.active_tab_index], control_value=control_value
                    )
                # Clear the input after processing the command
                self.uav_update_commands[uav_index - 1].clear()

        except Exception as e:
            self.popup_msg(
                f"Invalid input: {repr(e)}", src_msg="process_command", type_msg="Error"
            )

    # -----------------------< UAV buttons callback functions >-----------------------
    async def uav_connect_callback(self, uav_index) -> None:
        """
        Asynchronously connects to a UAV or all UAVs.

        Args:
            uav_index (int): The index of the UAV to connect to. If 0, connects to all UAVs.

        Raises:
            Exception: If there is an error during the connection process.
        """
        global UAVs

        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not UAVs[uav_index]["connection_allow"]:
                self.update_terminal(f"[INFO] Connection not allowed for UAV {uav_index}")
                return
            try:
                self.update_terminal(f"[INFO] Sent CONNECT command to UAV {uav_index}")
                # set default information
                UAVs[uav_index]["status"]["connection_status"] = False
                self.set_connection_display(uav_index, UAVs[uav_index]["status"])

                # 1 init server
                if UAVs[uav_index]["server"]["start"]:
                    UAVs[uav_index]["server"]["shell"].stop()
                    UAVs[uav_index]["server"]["start"] = False
                    await asyncio.sleep(1)

                UAVs[uav_index]["server"]["shell"].start()
                UAVs[uav_index]["server"]["start"] = True

                await asyncio.sleep(5)
                # 2 connect to system
                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )

                logger.log(f"Waiting for drone {uav_index} to connect...", level="info")
                # 3 check connection status
                async for state in UAVs[uav_index]["system"].core.connection_state():
                    if state.is_connected:
                        logger.log(f"UAV-{uav_index} -- Connected", level="info")
                        self.update_terminal(
                            f"[INFO] Received CONNECT signal from UAV {uav_index}"
                        )
                        UAVs[uav_index]["status"]["connection_status"] = True
                    else:
                        logger.log(f"UAV-{uav_index} -- Disconnected", level="info")
                        self.update_terminal(
                            f"[INFO] Cannot receive CONNECT signal from UAV {uav_index}"
                        )
                        UAVs[uav_index]["status"]["connection_status"] = False
                    break
                # 4 update connection status
                self.set_connection_display(uav_index, UAVs[uav_index]["status"])
                # 5 overwrite params file
                await uav_fn_overwrite_params(
                    UAVs[uav_index], parameters=OVERWRITE_PARAMS[uav_index]
                )
                # 5 export params file
                await uav_fn_export_params(
                    drone=UAVs[uav_index], save_path=parameter_data_files[uav_index - 1]
                )
                # 6 continuously update status
                await self.uav_fn_get_status(uav_index)

            except Exception as e:
                UAVs[uav_index]["status"]["connection_status"] = False
                self.set_connection_display(uav_index, UAVs[uav_index]["status"])
                logger.log(f"Connection error to uav {uav_index} :{repr(e)}", level="error")
                self.popup_msg(
                    f"Connection error to uav {uav_index} :{repr(e)}",
                    src_msg="uav_connect_callback",
                    type_msg="error",
                )

        else:
            connect_all_UAVs = [
                self.uav_connect_callback(uav_index) for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*connect_all_UAVs)

    async def uav_arm_callback(self, uav_index) -> None:
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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent ARM command to UAV {uav_index}")
                #
                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )
                await UAVs[uav_index]["system"].action.arm()
                await asyncio.sleep(3)
                await self.uav_disarm_callback(uav_index)

                UAVs[uav_index]["status"]["arming_status"] = "ARMED"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                UAVs[uav_index]["status"]["arming_status"] = "DISARMED"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(f"Error: {repr(e)}", src_msg="uav_arm_callback", type_msg="Error")
        else:
            arm_all_UAVs = [
                self.uav_arm_callback(uav_index) for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*arm_all_UAVs)

    async def uav_disarm_callback(self, uav_index) -> None:
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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent DISARM command to UAV {uav_index}")

                await UAVs[uav_index]["system"].action.disarm()

                UAVs[uav_index]["status"]["arming_status"] = "DISARMED"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_disarm_callback", type_msg="Error"
                )
        else:
            disarm_all_UAVs = [
                self.uav_disarm_callback(uav_index) for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*disarm_all_UAVs)

    async def uav_takeoff_callback(self, uav_index) -> None:
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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent TAKEOFF command to UAV {uav_index}")

                await UAVs[uav_index]["system"].connect(
                    system_address=UAVs[uav_index]["system_address"]
                )
                await UAVs[uav_index]["system"].action.arm()
                await UAVs[uav_index]["system"].action.takeoff()

                # # update initial position of UAV

                UAVs[uav_index]["init_params"]["latitude"] = float(
                    UAVs[uav_index]["status"]["position_status"][0]
                )
                UAVs[uav_index]["init_params"]["longitude"] = float(
                    UAVs[uav_index]["status"]["position_status"][1]
                )

                # save initial position to file
                with open(drone_init_pos_files[uav_index - 1], "w") as f:
                    f.write(
                        f"{UAVs[uav_index]['init_params']['latitude']}, {UAVs[uav_index]['init_params']['longitude']}"
                    )

                # update UAV information
                UAVs[uav_index]["status"]["connection_status"] = True
                UAVs[uav_index]["status"]["mode_status"] = "TAKING OFF"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_takeoff_callback", type_msg="Error"
                )

        else:
            # NOTE: uav_index = 0, take off all available UAVs
            takeoff_all_UAVs = [
                self.uav_takeoff_callback(uav_index) for uav_index in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*takeoff_all_UAVs)

    async def uav_land_callback(self, uav_index) -> None:
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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent LANDING command to UAV {uav_index}")

                await UAVs[uav_index]["system"].action.land()

                UAVs[uav_index]["status"]["mode_status"] = "LANDING"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(f"Error: {repr(e)}", src_msg="uav_land_callback", type_msg="Error")

        else:
            # NOTE: uav_index = 0, land all available UAVs
            landing_all_UAVs = [
                self.uav_land_callback(uav_index) for uav_index in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*landing_all_UAVs)

    async def uav_return_callback(self, uav_index, rtl=False) -> None:
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

        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                # if return to launch, which means the UAV will return to the initial position and land
                init_latitude = UAVs[uav_index]["init_params"]["latitude"]
                init_longitude = UAVs[uav_index]["init_params"]["longitude"]
                current_latitude = UAVs[uav_index]["status"]["position_status"][0]
                current_longitude = UAVs[uav_index]["status"]["position_status"][1]

                if rtl:
                    self.update_terminal(f"[INFO] Sent RTL command to UAV {uav_index}")
                    if (init_latitude, init_longitude) == (current_latitude, current_longitude):
                        self.update_terminal(
                            f"[INFO] UAV {uav_index} is already at the initial position, landing..."
                        )
                        await UAVs[uav_index]["system"].action.land()
                    else:
                        await UAVs[uav_index]["system"].action.return_to_launch()

                    UAVs[uav_index]["status"]["mode_status"] = "RTL"
                    self.uav_information_views[uav_index - 1].setText(
                        self.template_information(uav_index, **UAVs[uav_index]["status"])
                    )
                else:  # return to initial position
                    self.update_terminal(
                        f"[INFO] Sent RETURN command to UAV {uav_index} to lat: {init_latitude} long: {init_longitude}"
                    )

                    await uav_fn_goto_location(
                        drone=UAVs[uav_index],
                        latitude=init_latitude,
                        longitude=init_longitude,
                    )

                    UAVs[uav_index]["status"]["mode_status"] = "RETURN"
                    self.uav_information_views[uav_index - 1].setText(
                        self.template_information(uav_index, **UAVs[uav_index]["status"])
                    )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_return_callback", type_msg="Error"
                )
        else:
            # NOTE: uav_index = 0, return all UAVs
            return_all_UAVs = [
                self.uav_return_callback(uav_index, rtl=rtl)
                for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*return_all_UAVs)

    async def uav_mission_callback(self, uav_index) -> None:
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
        if uav_index in AVAIL_UAV_INDEXES:
            if not (
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                # Health check before mission
                self.update_terminal(
                    "Waiting for drone to have a global position estimate...", uav_index=uav_index
                )
                async for health in UAVs[uav_index]["system"].telemetry.health():
                    if health.is_global_position_ok and health.is_home_position_ok:
                        logger.log(
                            f"UAV-{uav_index} -- Global position for estimate OK", level="info"
                        )
                        break

                # clear detection log files
                detection_log_files = glob.glob(f"{__current_path__}/logs/rescue_pos/*.log")
                for f in detection_log_files:
                    os.remove(f)

                # start new mission
                self.update_terminal(f"[INFO] Sent MISSION command to UAV {uav_index}")

                UAVs[uav_index]["status"]["on_mission"] = True

                await uav_fn_do_mission(
                    drone=UAVs[uav_index],
                    mission_plan_file=f"{__current_path__}/logs/points/reduced_point{uav_index}.txt",
                )

                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
                # clear mission log files
                if await UAVs[uav_index]["system"].mission.is_mission_finished():
                    await UAVs[uav_index]["system"].action.return_to_launch()
                    # remove rescue file and detected files
                    if os.path.exists(
                        f"{__current_path__}/logs/rescue_pos/rescue_pos_uav_{uav_index}.log"
                    ):
                        os.remove(
                            f"{__current_path__}/logs/rescue_pos/rescue_pos_uav_{uav_index}.log"
                        )
                    if os.path.exists(
                        f"{__current_path__}/logs/detected_pos/detection_pos_uav_{uav_index}.log"
                    ):
                        os.remove(
                            f"{__current_path__}/logs/detected_pos/detection_pos_uav_{uav_index}.log"
                        )

            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_mission_callback", type_msg="Error"
                )
        elif uav_index == RESCUE_UAV_INDEX:
            await self.uav_fn_rescue()

        else:
            # NOTE: uav_index = 0, mission all available UAVs
            mission_all_UAVs = [
                self.uav_mission_callback(uav_index) for uav_index in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*mission_all_UAVs)

    async def uav_push_mission_callback(self, uav_index) -> None:
        """
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

        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent PUSH MISSION command to UAV {uav_index}")

                if not os.path.exists(plans_log_dir):
                    logger.log(f"Directory {plans_log_dir} does not exist", level="error")

                # read mission points from file
                fpath = QFileDialog.getOpenFileName(
                    parent=self,
                    caption="Open file",
                    directory=str(__current_path__),
                    initialFilter="Files (*.TXT *.txt)",
                )[0]
                # push mission to UAV
                await uav_fn_upload_mission(drone=UAVs[uav_index], mission_plan_file=fpath)
                #
                UAVs[uav_index]["status"]["mode_status"] = "Mission pushing"
                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Mission error: {repr(e)}", src_msg="uav_mission_callback", type_msg="error"
                )
        else:
            self.popup_msg(
                msg="Buttons are disabled on this tab",
                type_msg="warning",
                src_msg="uav_push_mission_callback",
            )

    async def uav_toggle_pause_mission_callback(self, uav_index) -> None:
        """
        Pauses the mission of a specified UAV or all UAVs if the index is 0.

        Args:
            uav_index (int): The index of the UAV to pause. If 0, pauses all UAVs.
        """
        # NOTE: add toggle for mission pause and resume
        global UAVs
        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                if UAVs[uav_index]["status"]["on_mission"]:
                    self.update_terminal(f"[INFO] Sent PAUSE command to UAV {uav_index}")

                    await UAVs[uav_index]["system"].mission.pause_mission()
                    #
                    UAVs[uav_index]["status"]["on_mission"] = False
                else:
                    self.update_terminal(f"[INFO] Sent RESUME command to UAV {uav_index}")

                    await UAVs[uav_index]["system"].mission.start_mission()
                    #
                    UAVs[uav_index]["status"]["on_mission"] = True

                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_pause_mission_callback", type_msg="Error"
                )

        else:
            # NOTE: uav_index = 0, pause all UAVs
            pauseMission_all_UAVs = [
                self.uav_toggle_pause_mission_callback(uav_index)
                for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*pauseMission_all_UAVs)

    async def uav_toggle_open_callback(self, uav_index) -> None:
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
                UAVs[uav_index]["status"]["connection_status"]
                and UAVs[uav_index]["connection_allow"]
            ):
                return
            try:
                self.update_terminal(f"[INFO] Sent OPEN/CLOSE command to UAV {uav_index}")

                if UAVs[uav_index]["status"]["actuator_status"]:
                    # ====== replace with your function
                    await uav_fn_control_gimbal(
                        drone=UAVs[uav_index], control_value={"pitch": 90, "yaw": 0}
                    )
                    # ======
                    UAVs[uav_index]["status"]["actuator_status"] = False
                else:
                    # ====== replace with your function
                    await uav_fn_control_gimbal(
                        drone=UAVs[uav_index], control_value={"pitch": -90, "yaw": 0}
                    )
                    # ======
                    UAVs[uav_index]["status"]["actuator_status"] = True

                self.uav_information_views[uav_index - 1].setText(
                    self.template_information(uav_index, **UAVs[uav_index]["status"])
                )
            except Exception as e:
                logger.log(f"Error: {repr(e)}", level="error")
                self.popup_msg(
                    f"Error: {repr(e)}", src_msg="uav_toggle_open_callback", type_msg="Error"
                )

        else:
            openClose_all_UAVs = [
                self.uav_toggle_open_callback(uav_index)
                for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*openClose_all_UAVs)

    def uav_toggle_camera_callback(self, uav_index) -> None:
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
        global UAVs

        if uav_index in range(1, MAX_UAV_COUNT + 1):
            if not (
                (
                    UAVs[uav_index]["connection_allow"]
                    or UAVs[uav_index]["status"]["connection_status"]
                )
                and UAVs[uav_index]["streaming_enable"]
            ):
                return
            try:
                # check if the UAV is streaming, if yes, stop the streaming, otherwise start the streaming
                if not UAVs[uav_index]["status"]["streaming_status"]:
                    if self.uav_stream_threads[uav_index - 1] is None:
                        self._create_streaming_threads(uav_indexes=[uav_index])
                    # start the steaming thread
                    self.uav_stream_threads[uav_index - 1].start()
                    UAVs[uav_index]["status"]["streaming_status"] = True
                    # set steaming status
                    logger.log(f"UAV-{uav_index} streaming thread is starting...", level="info")
                    self.ui.btn_toggle_camera.setStyleSheet("background-color : green")
                else:
                    # stop the steaming thread
                    self.uav_stream_threads[uav_index - 1].stop()
                    UAVs[uav_index]["status"]["streaming_status"] = False
                    # set steaming status
                    logger.log(
                        f"UAV-{uav_index} streaming thread is paused...",
                        level="info",
                    )
                    self.ui.btn_toggle_camera.setStyleSheet("background-color : red")

                self.uav_stream_threads[uav_index - 1].isRunning = UAVs[uav_index]["status"][
                    "streaming_status"
                ]

            except Exception as e:
                logger.log(repr(e), level="error")
                self.popup_msg(type_msg="Error", msg=repr(e), src_msg="uav_toggle_camera_callback")
        else:
            for uav_index in range(1, MAX_UAV_COUNT + 1):
                self.uav_toggle_camera_callback(uav_index)

    async def uav_goto_callback(self, uav_index, page="settings", *args) -> None:
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
        global UAVs
        try:
            default_longitude = UAVs[uav_index]["init_params"]["longitude"] + uav_index * 0.0001
            default_latitude = UAVs[uav_index]["init_params"]["latitude"]

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
                await uav_fn_goto_location(
                    drone=UAVs[uav_index], latitude=latitude, longitude=longitude
                )
            else:
                goTo_all_UAVs = [
                    uav_fn_goto_location(
                        drone=UAVs[uav_index], latitude=latitude, longitude=longitude
                    )
                    for uav_index in range(1, MAX_UAV_COUNT + 1)
                ]
                await asyncio.gather(*goTo_all_UAVs)
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Go to error: {repr(e)}", src_msg="uav_goto_callback", type_msg="error"
            )

    # --------------------------<UAVs get status functions>-----------------------------
    async def uav_fn_get_position(self, uav_index) -> None:
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
            alt_rel = round(position.relative_altitude_m, 12)
            alt_msl = round(position.absolute_altitude_m, 12)
            latitude = round(position.latitude_deg, 12)
            longitude = round(position.longitude_deg, 12)

            # update UAVs information
            UAVs[uav_index]["status"]["altitude_status"] = [
                alt_rel,
                alt_msl,
            ]
            UAVs[uav_index]["status"]["position_status"] = [
                latitude,
                longitude,
            ]

            self.uav_information_views[uav_index - 1].setText(
                self.template_information(uav_index, **UAVs[uav_index]["status"])
            )

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
            UAVs[uav_index]["status"]["mode_status"] = mode_status
            self.uav_information_views[uav_index - 1].setText(
                self.template_information(uav_index, **UAVs[uav_index]["status"])
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
            UAVs[uav_index]["status"]["battery_status"] = str(battery_status) + "%"
            self.uav_information_views[uav_index - 1].setText(
                self.template_information(uav_index, **UAVs[uav_index]["status"])
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
            UAVs[uav_index]["status"]["arming_status"] = arm_status
            self.uav_information_views[uav_index - 1].setText(
                self.template_information(uav_index, **UAVs[uav_index]["status"])
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
            UAVs[uav_index]["status"]["gps_status"] = gps_status
            self.uav_information_views[uav_index - 1].setText(
                self.template_information(uav_index, **UAVs[uav_index]["status"])
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

        parameters = await uav_fn_get_params(
            drone=UAVs[uav_index],
            list_params=displayed_parameter_list,
        )
        # update display fields
        for i, (_, value) in enumerate(parameters.items()):
            self.uav_param_displays[uav_index - 1].children()[i + 1].setText(str(round(value, 1)))

        if copy:  # copy parameters from display fields to set fields
            for i, (_, value) in enumerate(parameters.items()):
                self.uav_param_sets[uav_index - 1].children()[i + 1].setText(str(round(value, 1)))

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

        parameters = {}

        for i, (new_value, value) in enumerate(
            zip(
                self.uav_param_sets[uav_index - 1].children()[1:-1],
                self.uav_param_displays[uav_index - 1].children()[1:-1],
            )
        ):
            if new_value.text() == "":
                parameters[displayed_parameter_list[i]] = value.text()
            else:
                parameters[displayed_parameter_list[i]] = float(new_value.text())

        await uav_fn_set_params(
            drone=UAVs[uav_index],
            parameters=parameters,
            param_file=parameter_data_files[uav_index - 1],
        )

        await self.uav_fn_get_flight_info(uav_index=uav_index, copy=False)

    def set_connection_display(self, uav_index, uav_status):
        """
        Updates the connection status of a UAV in the UI.

        Args:
            uav_index (int): The index of the UAV to update.
            status (bool): The connection status of the UAV.

        Returns:
            None
        """
        if uav_status["connection_status"]:
            self.uav_label_params[uav_index - 1].setStyleSheet("background-color: green")
        else:
            self.uav_label_params[uav_index - 1].setStyleSheet("background-color: red")

        self.uav_information_views[uav_index - 1].setText(
            self.template_information(uav_index, **uav_status)
        )

    async def uav_fn_get_status(self, uav_index, verbose=1) -> None:
        global UAVs

        if uav_index in range(1, MAX_UAV_COUNT + 1):
            try:
                function_list = [
                    self.uav_fn_get_position(uav_index),
                    self.uav_fn_get_mode(uav_index),
                    self.uav_fn_get_battery(uav_index),
                    self.uav_fn_get_arm_status(uav_index),
                    self.uav_fn_get_gps(uav_index),
                    self.uav_fn_get_flight_info(uav_index, copy=False),
                ]
                if verbose:
                    function_list.append(self.uav_fn_printStatus(uav_index))

                await asyncio.gather(*function_list)
            except Exception as e:
                UAVs[uav_index]["status"]["connection_status"] = False
                self.set_connection_display(uav_index, UAVs[uav_index]["status"])
                self.popup_msg(
                    f"Get status error: {repr(e)}", src_msg="uav_fn_get_status", type_msg="error"
                )
        else:
            get_status_all_UAVs = [
                self.uav_fn_get_status(uav_index, verbose=verbose)
                for uav_index in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*get_status_all_UAVs)

    async def uav_fn_printStatus(self, uav_index) -> None:
        """
        Asynchronously prints the status of a UAV to the terminal.

        Args:
            uav_index (int): The index of the UAV in the global UAVs list.

        Returns:
            None
        """
        global UAVs
        if not (
            UAVs[uav_index]["status"]["connection_status"] and UAVs[uav_index]["connection_allow"]
        ):
            return

        async for status in UAVs[uav_index]["system"].telemetry.status_text():
            status = f"> {status.type} - {status.text}"
            self.update_terminal(status, uav_index)

    # -----------------------------< UAVs streaming functions >-----------------------------
    @pyqtSlot(np.ndarray, np.ndarray, list)
    def stream_on_uav_screen(self, frame=None, annotated_frame=None, results=None) -> None:
        """
        Display video stream on the UAV screen with optional object detection annotations.

        This method manages the streaming of video frames to the UAV interface. It can display
        either raw frames or annotated frames with detection results. The method also handles
        frame rate limitation to maintain reasonable performance and can export detected target
        information when objects of interest are found.

        Parameters:
        ----------
        frame : numpy.ndarray, optional
            The original video frame without annotations
        annotated_frame : numpy.ndarray, optional
            The video frame with detection annotations (bounding boxes, labels, etc.)
        results : tuple, optional
            Contains (uav_index, current_fps, detected_results) where:
            - uav_index: ID of the UAV
            - current_fps: Current frames per second rate
            - detected_results: Object detection results including track IDs and object data

        Returns:
        -------
        None
            This method doesn't return a value but updates the UAV screen display
            and may export detection data to logs.

        Notes:
        -----
        - The method only processes frames if UAV connection is allowed and streaming is enabled
        - Frame rate is limited according to DEFAULT_STREAM_FPS
        - When detection is enabled and a person is detected, the frame is saved and GPS coordinates
          are exported to logs
        """

        global UAVs
        uav_index, current_fps, detected_results = results
        uav_index = int(uav_index)
        max_frame_cnt = (
            current_fps // DEFAULT_STREAM_FPS if current_fps > DEFAULT_STREAM_FPS else 1
        )  # limit the frame rate
        if not (
            (UAVs[uav_index]["connection_allow"] or UAVs[uav_index]["status"]["connection_status"])
            and UAVs[uav_index]["streaming_enable"]
        ):
            return
        try:
            streaming_frame = annotated_frame if UAVs[uav_index]["detection_enable"] else frame

            # limit the frame rate of stream
            self.uav_stream_frame_cnt[uav_index - 1] += 1
            if self.uav_stream_frame_cnt[uav_index - 1] % int(max_frame_cnt) != 0:
                return

            # update the UAV screen view
            self.update_uav_screen_view(
                uav_index, streaming_frame, screen_name=DEFAULT_STREAM_SCREEN
            )

            if UAVs[uav_index]["detection_enable"]:
                if len(detected_results) != 2:
                    return

                track_ids, objects = detected_results
                for track_id, obj in zip(track_ids, objects):
                    if obj["detected"] and obj["class"] == "person":
                        # export frame
                        cv2.imwrite(
                            f"{__current_path__}/logs/images/UAV{uav_index}_locked_target_{track_id}.png",
                            annotated_frame,
                        )
                        detected_pos = (obj["x"], obj["y"])
                        frame_shape = annotated_frame.shape
                        uav_lat, uav_long = UAVs[uav_index]["status"]["position_status"]
                        uav_alt = UAVs[uav_index]["status"]["altitude_status"][0]
                        uav_gps = [uav_lat, uav_long, uav_alt]
                        self.update_terminal(
                            f"UAV-{uav_index} at gps ({uav_gps[0]}, {uav_gps[1]}, {uav_gps[2]}) detect {obj['class']} at X: {detected_pos[0]} Y: {detected_pos[1]} with frame size: {frame_shape}",
                            0,
                        )
                        export_points_to_gps_log(
                            uav_index=uav_index,
                            detected_pos=detected_pos,
                            frame_shape=frame_shape,
                            uav_gps=uav_gps,
                        )
                        UAVs[uav_index]["detection_enable"] = False

        except Exception as e:
            UAVs[uav_index]["status"]["streaming_status"] = False
            self.popup_msg(
                f"Stream on UAV screen error: {repr(e)}",
                src_msg="stream_on_uav_screen",
                type_msg="error",
            )

    # ------------------------------------< Rescue UAV 6 >-----------------------------

    async def uav_fn_rescue(self) -> None:
        """
        Perform a rescue mission using the specified UAV.
        This function checks the connection status of the rescue UAV, connects to it,
        verifies its health, and retrieves its initial position. It then performs the
        rescue mission if certain conditions are met.
        The rescue mission involves:
        1. Checking if rescue position logs are available.
        2. Selecting a mission plan from the available logs.
        3. Performing the rescue mission and suspending detected UAVs.
        4. Removing the rescue log file after the mission is completed.
        If any error occurs during the mission, it logs the error and displays a popup message.
        Returns:
            None
        """

        global UAVs
        if not (
            UAVs[RESCUE_UAV_INDEX]["status"]["connection_status"]
            and UAVs[RESCUE_UAV_INDEX]["connection_allow"]
        ):
            return

        self.update_terminal(f"[INFO] Sent RESCUE command to UAV {RESCUE_UAV_INDEX}")

        await UAVs[RESCUE_UAV_INDEX]["system"].connect(
            system_address=UAVs[RESCUE_UAV_INDEX]["system_address"]
        )
        # check health
        async for health in UAVs[RESCUE_UAV_INDEX]["system"].telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                logger.log(
                    f"UAV-{RESCUE_UAV_INDEX} -- Global position for estimate OK", level="info"
                )
                break

        logger.log(f"UAV-{RESCUE_UAV_INDEX} -- Arming and taking off", level="info")

        await asyncio.sleep(1)
        await UAVs[RESCUE_UAV_INDEX]["system"].action.arm()
        await asyncio.sleep(2)
        await UAVs[RESCUE_UAV_INDEX]["system"].action.takeoff()
        await asyncio.sleep(3)

        # get initial position
        async for position in UAVs[RESCUE_UAV_INDEX]["system"].telemetry.position():
            UAVs[RESCUE_UAV_INDEX]["init_params"]["latitude"] = round(position.latitude_deg, 12)
            UAVs[RESCUE_UAV_INDEX]["init_params"]["longitude"] = round(position.longitude_deg, 12)
            break

        try:
            # do the rescue mission
            while True:
                # NOTE 1st time rescue mission or press mission btn 6
                if not UAVs[RESCUE_UAV_INDEX]["rescue_first_time"] and not (
                    self.ui.tabWidget.currentIndex() == RESCUE_UAV_INDEX
                ):
                    return

                # 1 check if rescue position is available
                rescue_filepaths = glob.glob(
                    f"{__current_path__}/logs/rescue_pos/rescue_pos_uav_*.log"
                )

                if len(rescue_filepaths) == 0:
                    logger.log(
                        f"No rescue position found, re-check rescue directory...", level="info"
                    )
                    await asyncio.sleep(1)
                    continue

                # get the rescue filepath
                # NOTE: you can implement your own logic here
                rescue_filepath = select_mission_plan(rescue_filepaths)
                logger.log(
                    f"Found {len(rescue_filepaths)} rescue files, select: {rescue_filepath}",
                    level="info",
                )

                # get the detected UAVs
                detected_uav_list = []
                for rescue_filepath in rescue_filepaths:
                    uav_index = int(Path(rescue_filepath).stem.split("_")[-1])
                    detected_uav_list.append(UAVs[uav_index])

                logger.log("Rescue mission started...", level="info")

                # 2 UAV Rescue do the rescue mission and the detected drones goes into suspend mode
                UAVs[RESCUE_UAV_INDEX]["status"]["on_mission"] = True
                await asyncio.gather(
                    uav_suspend_missions(drones=detected_uav_list, suspend_time=30),
                    uav_rescue_process(
                        drone=UAVs[RESCUE_UAV_INDEX], rescue_filepath=rescue_filepath
                    ),
                )
                UAVs[RESCUE_UAV_INDEX]["status"]["on_mission"] = False

                # 3 remove the rescue file
                os.remove(rescue_filepath)  # remove the rescue file

                break  # remove this line if you want to do the rescue mission continuously

            logger.log(f"Rescue mission completed", level="info")
        except Exception as e:
            logger.log(f"Error: {repr(e)}", level="error")
            self.popup_msg(f"Error: {repr(e)}", src_msg="uav_fn_rescue", type_msg="Error")


# ------------------------------------< Main Application Class >-----------------------------
def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Oxygen")  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = App()
    MainWindow.show()

    with loop:
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
