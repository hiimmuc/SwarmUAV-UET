import asyncio
import glob
import os
import sys
from datetime import datetime

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
__version__ = "3.20.0"
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
                "shell": MAVSDKServer(
                    id=uav_index,
                    protocol=PROTOCOLS[uav_index - 1],
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
            "rescue_first_time": True,
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
        Initialize the application components and configure default settings.
        
        This method sets up the UI, connections, and configuration required for the application
        to run properly. It performs the following tasks:
        1. Sets the default view tabs
        2. Configures button click events
        3. Sets up line edit events
        4. Creates streaming threads
        5. Initializes settings and UI components
        """
        logger.log("Initializing application components...", level="info")
        
        # Set default UI views
        self._init_interface_views()
        
        # Setup event handlers
        self._init_event_handlers()
        
        # Create streaming components
        self._create_streaming_threads()
        
        # Configure settings
        self._handling_settings(mode="init")
    
    def _init_interface_views(self) -> None:
        """
        Set up the initial UI views and default tab selections.
        
        This configures the default screens and tabs that are shown when
        the application first starts.
        """
        # Set main view to the first page
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # Set the tab view to the first tab
        self.ui.tabWidget.setCurrentIndex(0)
        
        # Configure initial status indicators
        self._update_status_indicators()

    def _init_event_handlers(self) -> None:
        """
        Initialize all event handlers for UI components.
        
        This sets up the connections between UI elements (buttons, line edits)
        and their corresponding handler functions.
        """
        # Connect button click events
        self._button_clicked_event()
        
        # Connect line edit events
        self._line_edit_event()
        
        # Connect custom signals
        self._connect_custom_signals()
        
    def _update_status_indicators(self) -> None:
        """
        Update the status indicators for all UAVs.
        
        This updates the visual indicators showing the connection status,
        battery level, and other status information for each UAV.
        """
        # Update connection status indicators
        for uav_index in range(1, MAX_UAV_COUNT + 1):
            self.set_connection_display(uav_index, UAVs[uav_index]["status"])

    def _connect_custom_signals(self) -> None:
        """
        Connect custom Qt signals to their respective handler functions.
        
        This sets up signal connections for custom events like streaming
        updates and parameter changes.
        """
        # Add any additional signal connections here
        pass

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
        # Define button mappings for main control functions
        button_mappings = {
            self.ui.btn_arm: lambda: self.uav_arm_callback(self.active_tab_index),
            self.ui.btn_disarm: lambda: self.uav_disarm_callback(self.active_tab_index),
            self.ui.btn_open_close: lambda: self.uav_toggle_open_callback(self.active_tab_index),
            self.ui.btn_landing: lambda: self.uav_land_callback(self.active_tab_index),
            self.ui.btn_take_off: lambda: self.uav_takeoff_callback(self.active_tab_index),
            self.ui.btn_pause_resume: lambda: self.uav_toggle_pause_mission_callback(self.active_tab_index),
            self.ui.btn_connect: lambda: self.uav_connect_callback(self.active_tab_index),
            self.ui.btn_rtl: lambda: self.uav_return_callback(self.active_tab_index, rtl=True),
            self.ui.btn_return: lambda: self.uav_return_callback(self.active_tab_index, rtl=False),
            self.ui.btn_mission: lambda: self.uav_mission_callback(self.active_tab_index),
            self.ui.btn_push_mission: lambda: self.uav_push_mission_callback(self.active_tab_index),
        }
        
        # Connect main control buttons
        for button, callback in button_mappings.items():
            button.clicked.connect(lambda checked=False, cb=callback: asyncio.create_task(cb()))
        
        # Connect camera toggle button (non-async)
        self.ui.btn_toggle_camera.clicked.connect(
            lambda: self.uav_toggle_camera_callback(self.active_tab_index)
        )
        
        # Connect parameter buttons for each UAV
        self._connect_parameter_buttons()
        
        # Connect settings configuration buttons
        self.ui.btn_sett_cf_nSwarms.clicked.connect(
            lambda: self._handling_settings(mode="settings")
        )
        self.ui.btn_ovv_cf_nSwarms.clicked.connect(
            lambda: self._handling_settings(mode="overview")
        )
        
        # Connect GoTo navigation buttons
        self._connect_goto_buttons()
        
    def _connect_parameter_buttons(self) -> None:
        """
        Connect parameter control buttons for each UAV.
        
        This connects the set/get parameter buttons for all UAVs to
        the appropriate handler functions.
        """
        # Connect Set Parameter buttons
        for uav_index in range(1, MAX_UAV_COUNT + 1):
            idx = uav_index - 1  # Adjust for zero-based indexing
            
            # Create a closure to capture the current UAV index
            def create_set_callback(uav_idx):
                return lambda: asyncio.create_task(self.uav_fn_set_flight_info(uav_idx))
            
            def create_get_callback(uav_idx):
                return lambda: asyncio.create_task(self.uav_fn_get_flight_info(uav_idx, True))
            
            # Connect Set Parameter button
            self.uav_set_param_buttons[idx].clicked.connect(create_set_callback(uav_index))
            
            # Connect Get Parameter button
            self.uav_get_param_buttons[idx].clicked.connect(create_get_callback(uav_index))

    def _connect_goto_buttons(self) -> None:
        """
        Connect GoTo navigation buttons for each UAV.
        
        This connects the navigation buttons that send UAVs to specific
        GPS coordinates from the settings or overview pages.
        """
        # GoTo button mapping for settings and overview pages
        for uav_index in range(7):  # 0-6 for all UAVs plus all-UAV control
            # Create closures to capture the current UAV index
            def create_goto_settings_callback(uav_idx):
                return lambda: asyncio.create_task(
                    self.uav_goto_callback(uav_index=uav_idx, page="settings")
                )
            
            def create_goto_overview_callback(uav_idx):
                return lambda: asyncio.create_task(
                    self.uav_goto_callback(uav_index=uav_idx, page="overview")
                )
            
            # Connect Settings page GoTo button
            self.uav_sett_goTo_buttons[uav_index].clicked.connect(
                create_goto_settings_callback(uav_index)
            )
            
            # Connect Overview page GoTo button
            self.uav_ovv_goTo_buttons[uav_index].clicked.connect(
                create_goto_overview_callback(uav_index)
            )

    def _line_edit_event(self) -> None:
        """
        Connect line edit events to their handler functions.
        
        This connects the returnPressed event of command input fields
        to the process_command function for each UAV.
        """
        for index in range(MAX_UAV_COUNT):
            # Create a closure to capture the current UAV index
            def create_command_callback(uav_idx):
                return lambda: asyncio.create_task(self.process_command(uav_idx))
            
            # Connect the returnPressed event to the process_command function
            self.uav_update_commands[index].returnPressed.connect(
                create_command_callback(index + 1)
            )

    def _create_streaming_threads(self, uav_indexes=None) -> None:
        """
        Create and configure video streaming threads for UAVs.
        
        This method sets up streaming threads for specified UAVs, configuring capture
        settings, recording options, and object detection. It connects each thread's
        signal to the streaming display handler.
        
        Args:
            uav_indexes (list, optional): Specific UAV indexes to configure. 
                                        If None, configures all UAVs.
        
        Returns:
            None
        """
        global UAVs
        
        try:
            # If no specific indexes provided, use all available UAVs
            uav_indexes = range(1, MAX_UAV_COUNT + 1) if uav_indexes is None else uav_indexes
            
            for uav_index in uav_indexes:
                # Skip UAVs that aren't eligible for streaming
                if not self._can_stream(uav_index):
                    continue
                    
                # Configure stream settings
                stream_config = self._create_stream_config(uav_index)
                
                # Determine detection model if enabled
                detection_model = (
                    self.uav_detection_models[uav_index - 1]
                    if UAVs[uav_index]["detection_enable"]
                    else None
                )
                
                # Create the streaming thread
                self.uav_stream_threads[uav_index - 1] = StreamQtThread(
                    uav_index=uav_index,
                    stream_config=stream_config,
                    detection_model=detection_model
                )
                
                # Log the stream configuration
                self._log_stream_creation(uav_index)
                
                # Safely connect signal to slot (disconnect first to prevent duplicate connections)
                self._connect_stream_signal(uav_index)
                
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                type_msg="Error", 
                msg=repr(e), 
                src_msg="_create_streaming_threads()"
            )
            
    def _create_stream_config(self, uav_index):
        """Create stream configuration dictionary for a UAV"""
        global UAVs
        
        # Capture settings
        capture = {
            "index": uav_index,
            "address": UAVs[uav_index]["streaming_address"],
            "width": DEFAULT_STREAM_SIZE[0],
            "height": DEFAULT_STREAM_SIZE[1],
            "fps": DEFAULT_STREAM_FPS,
        }
        
        # Recording settings
        writer = {
            "index": uav_index,
            "enable": UAVs[uav_index]["recording_enable"],
            "filename": DEFAULT_STREAM_VIDEO_LOG_PATHS[uav_index - 1],
            "fourcc": FOURCC,
            "frameSize": DEFAULT_STREAM_SIZE,
        }
        
        return {
            "capture": capture,
            "writer": writer,
        }
        
    def _log_stream_creation(self, uav_index):
        """Log the creation of a streaming thread"""
        recording_path = (
            os.path.relpath(DEFAULT_STREAM_VIDEO_LOG_PATHS[uav_index - 1], __current_path__)
            if UAVs[uav_index]["recording_enable"]
            else 'None'
        )
        
        logger.log(
            f"UAV-{uav_index} stream started: \n"
            f"  -- Capture stream from {os.path.relpath(UAVs[uav_index]['streaming_address'], __current_path__)} \n"
            f"  -- Save recording to {recording_path}",
            level="info"
        )
        
        logger.log(f"UAV-{uav_index} streaming thread created!", level="info")
        
    def _connect_stream_signal(self, uav_index):
        """Connect the streaming thread signal to the display slot"""
        try:
            # Try to disconnect any existing connection to prevent duplicates
            self.uav_stream_threads[uav_index - 1].change_image_signal.disconnect()
        except Exception:
            # Ignore errors if there was no existing connection
            pass
            
        # Connect the signal to the slot with queued connection type
        self.uav_stream_threads[uav_index - 1].change_image_signal.connect(
            self.stream_on_uav_screen,
            Qt.QueuedConnection
        )
    # //-/////////////////////////////////////////////////////////////

    def _handling_settings(self, mode="init") -> None:
        """
        Handle configuration settings for the interface.
        
        This method manages configuration settings across different modes:
        - init: Load initial settings from configuration
        - settings: Apply settings from the Settings tab
        - overview: Apply settings from the Overview tab
        
        Args:
            mode (str): The mode to handle ('init', 'settings', or 'overview')
        """
        try:
            logger.log(f"Handling settings in '{mode}' mode", level="info")
            
            # Handle checkbox states and related UAV settings
            self._handling_checkboxes(mode=mode)
            
            # Handle table data and connection settings
            self._handling_tables(mode=mode)
            
        except Exception as e:
            logger.log(f"Error handling settings in '{mode}' mode: {e}", level="error")
            self.popup_msg(
                msg=f"Error handling settings: {e}", 
                src_msg="_handling_settings", 
                type_msg="Error"
            )

    def _handling_checkboxes(self, mode="init") -> None:
        """
        Handle checkbox states and update UAV detection/streaming settings.
        
        This method synchronizes checkbox states between UI elements and UAV settings
        based on the specified mode.
        
        Args:
            mode (str): The mode to handle ('init', 'settings', or 'overview')
            
        Returns:
            None
        """
        global UAVs
        
        try:
            if mode == "init":
                # Initialize UI checkboxes based on configuration
                for i, widget in enumerate(self.sett_checkBox_detect_lists):
                    widget.setChecked(UAVs[i + 1]["detection_enable"])
                    
                for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                    widget.setChecked(UAVs[i + 1]["detection_enable"])
                    
                for i, widget in enumerate(self.sett_checkBox_active_lists):
                    widget.setChecked(UAVs[i + 1]["streaming_enable"])
                    
            elif mode == "settings":
                # Update UAV settings from Settings page UI
                for i, widget in enumerate(self.sett_checkBox_detect_lists):
                    UAVs[i + 1]["detection_enable"] = widget.isChecked()
                    
                # Sync to Overview page
                for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                    widget.setChecked(UAVs[i + 1]["detection_enable"])
                    
                # Update streaming settings
                for i, widget in enumerate(self.sett_checkBox_active_lists):
                    UAVs[i + 1]["streaming_enable"] = widget.isChecked()
                    
            elif mode == "overview":
                # Update UAV settings from Overview page UI
                for i, widget in enumerate(self.ovv_checkBox_detect_lists):
                    UAVs[i + 1]["detection_enable"] = widget.isChecked()
                    
                # Sync to Settings page
                for i, widget in enumerate(self.sett_checkBox_detect_lists):
                    widget.setChecked(UAVs[i + 1]["detection_enable"])
                    
            logger.log(f"Checkbox settings updated in '{mode}' mode", level="debug")
            
        except Exception as e:
            logger.log(f"Error handling checkboxes in '{mode}' mode: {e}", level="error")
            self.popup_msg(
                msg=f"Error handling checkboxes: {e}", 
                src_msg="_handling_checkboxes", 
                type_msg="Error"
            )

    def _handling_tables(self, mode="init") -> None:
        """
        Update table data and related UAV connection settings.
        
        This method handles table data for UAV connection and streaming configuration
        according to the specified mode.
        
        Args:
            mode (str): The mode to handle ('init', 'settings', or 'overview')
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Common setup for all modes
            headers = ["id", "connection_address", "streaming_address"]
            connection_allow_indexes = self._get_enabled_uav_indexes("connection")
            streaming_enabled_indexes = self._get_enabled_uav_indexes("streaming")
            
            if mode == "init":
                # Prepare initial table data from configuration
                data = {
                    headers[0]: [uav_index for uav_index in range(1, MAX_UAV_COUNT + 1)],
                    headers[1]: [
                        f"{UAVs[uav_index]['system_address']} -p {UAVs[uav_index]['system']._port}"
                        for uav_index in range(1, MAX_UAV_COUNT + 1)
                    ],
                    headers[2]: [
                        UAVs[uav_index]['streaming_address']
                        for uav_index in range(1, MAX_UAV_COUNT + 1)
                    ],
                }
                nSwarms = len(connection_allow_indexes)
                
            else:
                # Get number of swarms from appropriate UI element
                if mode == "settings":
                    nSwarms = min(
                        int(self.ui.nSwarms_sett.value()), 
                        len(connection_allow_indexes)
                    )
                    data = get_values_from_table(self.ui.table_uav_large, headers=headers)
                else:  # overview mode
                    nSwarms = min(
                        int(self.ui.nSwarms_ovv.value()), 
                        len(connection_allow_indexes)
                    )
                    data = get_values_from_table(self.ui.table_uav_small, headers=headers)
                
                # Update UAV configuration from table data
                self._update_uav_config_from_table(data, connection_allow_indexes)
            
            # Update tables with current data
            self._update_tables(
                data=data,
                connection_allow_indexes=connection_allow_indexes,
                streaming_enabled_indexes=streaming_enabled_indexes,
                nSwarms=nSwarms,
                headers=headers,
            )
            
            logger.log(f"Table settings updated in '{mode}' mode", level="debug")
            
        except Exception as e:
            logger.log(f"Error handling tables in '{mode}' mode: {e}", level="error")
            self.popup_msg(
                msg=f"Error handling tables: {e}", 
                src_msg="_handling_tables", 
                type_msg="Error"
            )

    def _get_enabled_uav_indexes(self, feature_type):
        """
        Get indexes of UAVs with a specific feature enabled.
        
        Args:
            feature_type (str): The feature to check ('connection' or 'streaming')
            
        Returns:
            list: List of UAV indexes with the specified feature enabled
        """
        global UAVs
        
        if feature_type == "connection":
            return [
                index + 1 for index in range(MAX_UAV_COUNT) 
                if UAVs[index + 1]["connection_allow"]
            ]
        elif feature_type == "streaming":
            return [
                index + 1 for index in range(MAX_UAV_COUNT) 
                if UAVs[index + 1]["streaming_enable"]
            ]
        else:
            return []

    def _update_uav_config_from_table(self, data, connection_allow_indexes):
        """
        Update UAV configuration from table data.
        
        Args:
            data (dict): Table data containing connection and streaming addresses
            connection_allow_indexes (list): Indexes of UAVs with connection allowed
            
        Returns:
            None
        """
        global UAVs
        
        # Process each UAV's settings
        for index in range(MAX_UAV_COUNT):
            uav_index = index + 1
            if uav_index in connection_allow_indexes:
                # Parse connection address into components
                conn_address = data["connection_address"][index]
                address_parts, client_port = conn_address.split("-p")
                proto, server_parts = address_parts.split(":", 1)
                server_host = server_parts.split(":", 1)[0].replace("//", "")
                bind_port = server_parts.split(":", 1)[1] if ":" in server_parts else "0"
                
                # Update MAVSDK server configuration
                UAVs[uav_index]["server"]["shell"] = MAVSDKServer(
                    id=uav_index,
                    protocol=proto,
                    server_host=server_host,
                    port=int(client_port),
                    bind_port=int(bind_port),
                )
                
                # Update connection addresses
                UAVs[uav_index]["system_address"] = f"{proto}:{server_parts}"
                UAVs[uav_index]["system"]._port = int(client_port)
                
                # Update streaming address
                UAVs[uav_index]["streaming_address"] = data["streaming_address"][index].strip()
        
        # Reset connection and streaming status after configuration change
        for uav_index in range(1, MAX_UAV_COUNT + 1):
            UAVs[uav_index]["status"]["connection_status"] = False
            UAVs[uav_index]["status"]["streaming_status"] = False
        
        # Recreate streaming threads with new configuration
        self._create_streaming_threads()
        logger.log("Updated UAV configuration from table data", level="info")

    def _update_tables(
        self, data, connection_allow_indexes, streaming_enabled_indexes, nSwarms, headers
    ) -> None:
        """
        Update UAV tables with current configuration data.
        
        Args:
            data (dict): Table data to display
            connection_allow_indexes (list): Indexes of UAVs with connection allowed
            streaming_enabled_indexes (list): Indexes of UAVs with streaming enabled
            nSwarms (int): Number of swarm UAVs to display
            headers (list): Column headers for the table
            
        Returns:
            None
        """
        # Convert to DataFrame if needed
        df = pd.DataFrame.from_dict(data) if not isinstance(data, pd.DataFrame) else data
        
        # Update large table (settings page)
        draw_table(
            table_widget=self.ui.table_uav_large,
            data=df,
            connection_allow_indexes=connection_allow_indexes[:nSwarms],
            streaming_enabled_indexes=streaming_enabled_indexes,
            headers=headers,
        )
        
        # Update small table (overview page)
        draw_table(
            table_widget=self.ui.table_uav_small,
            data=df,
            connection_allow_indexes=connection_allow_indexes[:nSwarms],
            streaming_enabled_indexes=streaming_enabled_indexes,
            headers=headers,
        )
        
        # Update nSwarms value in both settings and overview pages
        self.ui.nSwarms_sett.setValue(nSwarms)
        self.ui.nSwarms_ovv.setValue(nSwarms)
        
        logger.log(f"Updated UAV tables with {nSwarms} swarms", level="debug")

    # ////////////////////////////////////////////////////////////////

    async def process_command(self, uav_index) -> None:
        """
        Processes a command for a specific UAV based on the given index.
        Args:
            uav_index (int): The index of the UAV to process the command for.
        Returns:
            None
        Raises:
            Exception: If an error occurs during command processing.
        The function performs the following steps:
        1. Checks if the UAV is connected and allowed to receive commands.
        2. Retrieves the command text from the corresponding UAV update command input.
        3. If the command is "hold", it instructs the UAV to hold its position.
        4. If the command is a movement or gimbal control command, it parses the command and value,
           and performs the corresponding action:
           - Movement commands: "forward", "backward", "left", "right", "up", "down"
           - Gimbal control commands: "pitch", "yaw"
        5. Clears the input after processing the command.
        6. Displays an error message if an invalid input is encountered.
        """
        global UAVs

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
        Asynchronous callback function to handle UAV connection. Connect to a specific UAV or all UAVs.
        
        It performs several steps:
        1. Initializes the server for the UAV.
        2. Connects to the UAV system and Checks the connection status.
        3. Updates the connection status display.
        4. Overwrites and exports UAV parameters.
        5. Continuously updates the UAV status.
        If the UAV index is not within the valid range, it attempts to connect to all UAVs.
        
        Args:
            uav_index (int): The UAV to connect to (1-MAX_UAV_COUNT), or 0 for all UAVs
            
        Returns:
            None
            
        Raises:
            Exception: If there is an error during the connection process, it logs the error and displays a popup message.
        """
        global UAVs

        # Handle the case of connecting to all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            connect_tasks = [
                self.uav_connect_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*connect_tasks)
            return

        # Skip if connection is not allowed
        if not UAVs[uav_index]["connection_allow"]:
            self.update_terminal(f"[INFO] Connection not allowed for UAV {uav_index}")
            return
            
        try:
            self.update_terminal(f"[INFO] Sent CONNECT command to UAV {uav_index}")
            
            # Reset connection status
            UAVs[uav_index]["status"]["connection_status"] = False
            self.set_connection_display(uav_index, UAVs[uav_index]["status"])

            # 1. Initialize server
            await self._initialize_server(uav_index)
            
            # 2. Connect to the UAV system
            await self._connect_to_system(uav_index)
            
            # 3. Update connection status display
            self.set_connection_display(uav_index, UAVs[uav_index]["status"])
            
            # 4. Configure UAV parameters
            await self._configure_uav_parameters(uav_index)
            
            # 5. Start continuous status updates
            await self.uav_fn_get_status(uav_index, verbose=True)

        except Exception as e:
            UAVs[uav_index]["status"]["connection_status"] = False
            self.set_connection_display(uav_index, UAVs[uav_index]["status"])
            logger.log(f"Connection error to UAV {uav_index}: {repr(e)}", level="error")
            self.popup_msg(
                f"Connection error to UAV {uav_index}: {repr(e)}",
                src_msg="uav_connect_callback",
                type_msg="error",
            )

    async def _initialize_server(self, uav_index):
        """Initialize the MAVSDK server for a UAV."""
        global UAVs
        
        if UAVs[uav_index]["server"]["start"]:
            UAVs[uav_index]["server"]["shell"].stop()
            UAVs[uav_index]["server"]["start"] = False
            await asyncio.sleep(1)

        UAVs[uav_index]["server"]["shell"].start()
        UAVs[uav_index]["server"]["start"] = True
        await asyncio.sleep(5)  # Allow time for server to start

    async def _connect_to_system(self, uav_index):
        """Connect to the UAV system and verify connection state."""
        global UAVs
        
        logger.log(f"Waiting for UAV {uav_index} to connect...", level="info")
        
        # 1. Connect to the system
        await UAVs[uav_index]["system"].connect(
            system_address=UAVs[uav_index]["system_address"]
        )
        
        # 2. Check connection status
        async for state in UAVs[uav_index]["system"].core.connection_state():
            if state.is_connected:
                logger.log(f"UAV-{uav_index} -- Connected", level="info")
                self.update_terminal(f"[INFO] Received CONNECT signal from UAV {uav_index}")
                UAVs[uav_index]["status"]["connection_status"] = True
            else:
                logger.log(f"UAV-{uav_index} -- Disconnected", level="info")
                self.update_terminal(f"[INFO] Cannot receive CONNECT signal from UAV {uav_index}")
                UAVs[uav_index]["status"]["connection_status"] = False
            break

    async def _configure_uav_parameters(self, uav_index):
        """Configure UAV parameters after connection."""
        global UAVs
        
        # Overwrite parameters from configuration
        await uav_fn_overwrite_params(
            UAVs[uav_index], parameters=OVERWRITE_PARAMS[uav_index]
        )
        
        # Set additional parameters manually
        await UAVs[uav_index]["system"].action.set_takeoff_altitude(
            altitude=UAVs[uav_index]["init_params"]["altitude"]
        )
        await UAVs[uav_index]["system"].action.set_current_speed(1.0)
        
        # Export parameters to file
        await uav_fn_export_params(
            drone=UAVs[uav_index], save_path=parameter_data_files[uav_index - 1]
        )

    async def uav_arm_callback(self, uav_index) -> None:
        """
        Arm a specific UAV or all UAVs.
        
        This method sends an ARM command to the specified UAV(s), waits for
        confirmation, and updates the arming status in the UI.
        
        Args:
            uav_index (int): The UAV to arm (1-MAX_UAV_COUNT), or 0 for all available UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of arming all available UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            arm_tasks = [
                self.uav_arm_callback(i) for i in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*arm_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            self.update_terminal(f"[INFO] Sent ARM command to UAV {uav_index}")
            
            # Ensure connection is established
            await UAVs[uav_index]["system"].connect(
                system_address=UAVs[uav_index]["system_address"]
            )
            
            # Send arm command
            await UAVs[uav_index]["system"].action.arm()
            await asyncio.sleep(3)
            
            # Temporarily disarm (may be application-specific behavior)
            await self.uav_disarm_callback(uav_index)
            
            # Update status
            UAVs[uav_index]["status"]["arming_status"] = "ARMED"
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            UAVs[uav_index]["status"]["arming_status"] = "DISARMED"
            self._update_uav_info_display(uav_index)
            logger.log(f"Arming error: {repr(e)}", level="error")
            self.popup_msg(f"Error: {repr(e)}", src_msg="uav_arm_callback", type_msg="Error")

    async def uav_disarm_callback(self, uav_index) -> None:
        """
        Disarm a specific UAV or all UAVs.
        
        This method sends a DISARM command to the specified UAV(s) and updates
        the arming status in the UI.
        
        Args:
            uav_index (int): The UAV to disarm (1-MAX_UAV_COUNT), or 0 for all UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of disarming all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            disarm_tasks = [
                self.uav_disarm_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*disarm_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            self.update_terminal(f"[INFO] Sent DISARM command to UAV {uav_index}")
            
            # Send disarm command
            await UAVs[uav_index]["system"].action.disarm()
            
            # Update status
            UAVs[uav_index]["status"]["arming_status"] = "DISARMED"
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Disarming error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error: {repr(e)}", src_msg="uav_disarm_callback", type_msg="Error"
            )

    async def uav_takeoff_callback(self, uav_index) -> None:
        """
        Initiate takeoff for a specific UAV or all UAVs.
        
        This method sends a TAKEOFF command to the specified UAV(s), arms the UAV,
        initiates takeoff, and updates the status in the UI.
        
        Args:
            uav_index (int): The UAV to command takeoff (1-MAX_UAV_COUNT), or 0 for all available UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of taking off all available UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            takeoff_tasks = [
                self.uav_takeoff_callback(i) for i in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*takeoff_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            self.update_terminal(f"[INFO] Sent TAKEOFF command to UAV {uav_index}")
            
            # Ensure connection is established
            await UAVs[uav_index]["system"].connect(
                system_address=UAVs[uav_index]["system_address"]
            )
            
            # Arm and take off
            await UAVs[uav_index]["system"].action.arm()
            await UAVs[uav_index]["system"].action.takeoff()
            
            # Save initial position information
            await self._save_initial_position(uav_index)
            
            # Update status
            UAVs[uav_index]["status"]["connection_status"] = True
            UAVs[uav_index]["status"]["mode_status"] = "TAKING OFF"
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Takeoff error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error: {repr(e)}", src_msg="uav_takeoff_callback", type_msg="Error"
            )

    async def _save_initial_position(self, uav_index):
        """Save the initial position of a UAV to a file."""
        # Update initial position from current position
        UAVs[uav_index]["init_params"]["latitude"] = round(
            UAVs[uav_index]["status"]["position_status"][0], 12
        )
        UAVs[uav_index]["init_params"]["longitude"] = round(
            UAVs[uav_index]["status"]["position_status"][1], 12
        )
        
        # Save to file
        with open(drone_init_pos_files[uav_index - 1], "w") as f:
            f.write(
                f"{UAVs[uav_index]['init_params']['latitude']}, {UAVs[uav_index]['init_params']['longitude']}"
            )

    async def uav_land_callback(self, uav_index) -> None:
        """
        Command a specific UAV or all UAVs to land.
        
        This method sends a LANDING command to the specified UAV(s) and updates
        the mode status in the UI.
        
        Args:
            uav_index (int): The UAV to command landing (1-MAX_UAV_COUNT), or 0 for all UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of landing all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            landing_tasks = [
                self.uav_land_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*landing_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            self.update_terminal(f"[INFO] Sent LANDING command to UAV {uav_index}")
            
            # Send land command
            await UAVs[uav_index]["system"].action.land()
            
            # Update status
            UAVs[uav_index]["status"]["mode_status"] = "LANDING"
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Landing error: {repr(e)}", level="error")
            self.popup_msg(f"Error: {repr(e)}", src_msg="uav_land_callback", type_msg="Error")

    async def uav_return_callback(self, uav_index, rtl=False) -> None:
        """
        Command a specific UAV or all UAVs to return.
        
        This method sends either a Return-To-Launch (RTL) command or a return to
        initial position command to the specified UAV(s) and updates the status in the UI.
        
        Args:
            uav_index (int): The UAV to command return (1-MAX_UAV_COUNT), or 0 for all available UAVs
            rtl (bool): If True, use RTL mode (land at return point), otherwise just return to position
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of returning all available UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            return_tasks = [
                self.uav_return_callback(i, rtl=rtl) for i in AVAIL_UAV_INDEXES
            ]
            await asyncio.gather(*return_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            # Get position information
            init_latitude = UAVs[uav_index]["init_params"]["latitude"]
            init_longitude = UAVs[uav_index]["init_params"]["longitude"]
            current_latitude = UAVs[uav_index]["status"]["position_status"][0]
            current_longitude = UAVs[uav_index]["status"]["position_status"][1]
            
            if rtl:
                # Return to launch (return and land)
                self.update_terminal(f"[INFO] Sent RTL command to UAV {uav_index}")
                
                # If already at initial position, just land
                if (init_latitude, init_longitude) == (current_latitude, current_longitude):
                    self.update_terminal(
                        f"[INFO] UAV {uav_index} is already at the initial position, landing..."
                    )
                    await UAVs[uav_index]["system"].action.land()
                else:
                    await UAVs[uav_index]["system"].action.return_to_launch()
                
                # Update status
                UAVs[uav_index]["status"]["mode_status"] = "RTL"
            else:
                # Return to initial position without landing
                self.update_terminal(
                    f"[INFO] Sent RETURN command to UAV {uav_index} to lat: {init_latitude} long: {init_longitude}"
                )
                
                # Go to the initial position
                await uav_fn_goto_location(
                    drone=UAVs[uav_index],
                    latitude=init_latitude,
                    longitude=init_longitude,
                )
                
                # Update status
                UAVs[uav_index]["status"]["mode_status"] = "RETURN"
            
            # Update display
            self._update_uav_info_display(uav_index)
            
            # Clean up mission logs
            clear_mission_logs(uav_index, save_dir=__current_path__)
            
        except Exception as e:
            logger.log(f"Return error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error: {repr(e)}", src_msg="uav_return_callback", type_msg="Error"
            )

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
        
        # Handle the case of missions for all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            mission_tasks = [
                self.uav_mission_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*mission_tasks)
            return
        
        # Handle regular UAV mission
        if uav_index in AVAIL_UAV_INDEXES:
            # await self._execute_standard_mission(uav_index)
            await asyncio.gather(
                self._execute_standard_mission(uav_index),
                # self.uav_fn_get_position(uav_index),
            )
        
        # Handle rescue UAV mission
        elif uav_index == RESCUE_UAV_INDEX:
            # Check if this is first time or if rescue tab is selected
            if not (UAVs[RESCUE_UAV_INDEX]["rescue_first_time"] or 
                    (self.ui.tabWidget.currentIndex() == RESCUE_UAV_INDEX)):
                return
            
            await self.uav_fn_rescue()
            
    async def _execute_standard_mission(self, uav_index):
        """Execute a standard mission for a regular UAV."""
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            # Health check before mission
            self.update_terminal(
                "Waiting for drone to have a global position estimate...", uav_index=uav_index
            )
            logger.log(f"UAV-{uav_index} -- Global position for estimate OK", level="info")
            
            # Clear detection log files
            detection_log_files = glob.glob(f"{__current_path__}/logs/rescue_pos/*.log")
            for f in detection_log_files:
                os.remove(f)
            
            # Start new mission
            self.update_terminal(f"[INFO] Sent MISSION command to UAV {uav_index}")
            UAVs[uav_index]["status"]["on_mission"] = True
            
            # Execute mission from plan file
            await uav_fn_do_mission(
                drone=UAVs[uav_index],
                mission_plan_file=f"{__current_path__}/logs/points/reduced_point{uav_index}.txt",
            )
            
            # Update display
            self._update_uav_info_display(uav_index)
            
            # Check if mission is finished and initiate return if needed
            if await UAVs[uav_index]["system"].mission.is_mission_finished():
                await UAVs[uav_index]["system"].action.return_to_launch()
                clear_mission_logs(uav_index, save_dir=__current_path__)
                
        except Exception as e:
            logger.log(f"Mission error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error: {repr(e)}", src_msg="uav_mission_callback", type_msg="Error"
            )
            
    async def uav_push_mission_callback(self, uav_index) -> None:
        """
        Push a mission to a specific UAV or all UAVs.
        
        This method uploads a mission from a selected file to the specified UAV(s).
        It allows the user to select a mission file via a file dialog and then
        uploads the mission to the UAV.
        
        Args:
            uav_index (int): The UAV to receive the mission (1-MAX_UAV_COUNT),
                            or 0 for all available UAVs
            
        Returns:
            None
            
        Raises:
            Exception: If there is an error during the mission push process.

        Notes:
            - Checks the connection status of the UAV.
            - Reads mission points from a user-selected file.
            - Uploads the mission and sets return to launch after mission.
            - Updates the UAV's mode status to 'Mission pushing'.
        """
        global UAVs
        
        # Handle the case of pushing missions to all available UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            # push_tasks = [
            #     self.uav_push_mission_callback(i) for i in AVAIL_UAV_INDEXES
            # ]
            # await asyncio.gather(*push_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            self.update_terminal(f"[INFO] Sent PUSH MISSION command to UAV {uav_index}")
            
            # Verify mission directory exists
            if not os.path.exists(plans_log_dir):
                logger.log(f"Mission directory {plans_log_dir} does not exist", level="warning")
                os.makedirs(plans_log_dir, exist_ok=True)
                
            # Open file dialog to select mission file
            mission_file = QFileDialog.getOpenFileName(
                parent=self,
                caption="Select Mission File",
                directory=str(__current_path__),
                initialFilter="Text Files (*.TXT *.txt)",
            )[0]
            
            if not mission_file:
                logger.log("Mission file selection canceled", level="info")
                return
                
            # Upload mission to UAV
            logger.log(f"Uploading mission from {mission_file} to UAV {uav_index}", level="info")
            await uav_fn_upload_mission(drone=UAVs[uav_index], mission_plan_file=mission_file)
            
            # Update status
            UAVs[uav_index]["status"]["mode_status"] = "Mission uploaded"
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Mission push error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error pushing mission: {repr(e)}",
                src_msg="uav_push_mission_callback",
                type_msg="Error"
            )

    async def uav_toggle_pause_mission_callback(self, uav_index) -> None:
        """
        Toggle pause/resume mission for a specific UAV or all UAVs.
        
        This method pauses an ongoing mission or resumes a paused mission
        for the specified UAV(s).
        
        Args:
            uav_index (int): The UAV to toggle mission state (1-MAX_UAV_COUNT),
                            or 0 for all UAVs
            
        Returns:
            None
        """

        global UAVs
        
        # Handle the case of toggling all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            toggle_tasks = [
                self.uav_toggle_pause_mission_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
            ]
            await asyncio.gather(*toggle_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            # Determine current mission state and toggle it
            is_on_mission = UAVs[uav_index]["status"]["on_mission"]
            
            if is_on_mission:
                # Pause the mission
                self.update_terminal(f"[INFO] Sent PAUSE MISSION command to UAV {uav_index}")
                await UAVs[uav_index]["system"].mission.pause_mission()
                UAVs[uav_index]["status"]["on_mission"] = False
                UAVs[uav_index]["status"]["mode_status"] = "Mission paused"
            else:
                # Resume the mission
                self.update_terminal(f"[INFO] Sent RESUME MISSION command to UAV {uav_index}")
                await UAVs[uav_index]["system"].mission.start_mission()
                UAVs[uav_index]["status"]["on_mission"] = True
                UAVs[uav_index]["status"]["mode_status"] = "Mission active"
            
            # Update display
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Mission toggle error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error toggling mission: {repr(e)}",
                src_msg="uav_toggle_pause_mission_callback",
                type_msg="Error"
            )

    async def uav_toggle_open_callback(self, uav_index) -> None:
        """
        Toggle actuator open/close state for a specific UAV or all UAVs.
        
        This method toggles the state of the actuator (e.g., payload, gripper)
        for the specified UAV(s) by controlling the gimbal pitch.
        
        Args:
            uav_index (int): The UAV to toggle actuator (1-MAX_UAV_COUNT),
                            or 0 for all UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of toggling all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            toggle_tasks = [
                self.uav_toggle_open_callback(i) for i in range(1, MAX_UAV_COUNT + 1)
                if UAVs[i]["connection_allow"]
            ]
            await asyncio.gather(*toggle_tasks)
            return
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
            
        try:
            # Determine current actuator state
            current_state = UAVs[uav_index]["status"]["actuator_status"]
            new_state = not current_state # Toggle state
            
            # Command based on the new state
            if new_state:
                # ======== Replace with the actual actuator control function ========
                # Open actuator (gimbal down)
                self.update_terminal(f"[INFO] Sent OPEN command to UAV {uav_index}")
                await uav_fn_control_gimbal(
                    drone=UAVs[uav_index], control_value={"pitch": -90, "yaw": 0}
                )
                # ====================================================================
            else:
                # ======== Replace with the actual actuator control function ========
                # Close actuator (gimbal up)
                self.update_terminal(f"[INFO] Sent CLOSE command to UAV {uav_index}")
                await uav_fn_control_gimbal(
                    drone=UAVs[uav_index], control_value={"pitch": 90, "yaw": 0}
                )
                # ====================================================================
            
            # Update status
            UAVs[uav_index]["status"]["actuator_status"] = new_state
            self._update_uav_info_display(uav_index)
            
        except Exception as e:
            logger.log(f"Actuator toggle error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error toggling actuator: {repr(e)}",
                src_msg="uav_toggle_open_callback",
                type_msg="Error"
            )

    def uav_toggle_camera_callback(self, uav_index) -> None:
        """
        Toggle camera streaming for a specific UAV or all UAVs.
        
        This method starts or stops the video streaming thread for the 
        specified UAV(s).
        
        Args:
            uav_index (int): The UAV to toggle camera (1-MAX_UAV_COUNT),
                            or 0 for all UAVs
            
        Returns:
            None
        """
        global UAVs
        
        # Handle the case of toggling all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            for i in range(1, MAX_UAV_COUNT + 1):
                # Only toggle UAVs that are eligible for streaming
                if self._can_stream(i):
                    self.uav_toggle_camera_callback(i)
            return
        
        # Skip if UAV is not eligible for streaming
        if not self._can_stream(uav_index):
            logger.log(
                f"Camera toggle skipped for UAV {uav_index}: not eligible for streaming",
                level="warning"
            )
            return
            
        try:
            # Determine current streaming state
            is_streaming = UAVs[uav_index]["status"]["streaming_status"]
            
            if not is_streaming:
                # Start streaming
                if self.uav_stream_threads[uav_index - 1] is None:
                    self._create_streaming_threads(uav_indexes=[uav_index])
                    
                self.uav_stream_threads[uav_index - 1].start()
                UAVs[uav_index]["status"]["streaming_status"] = True
                
                logger.log(f"UAV-{uav_index} streaming started", level="info")
                self.ui.btn_toggle_camera.setStyleSheet("background-color: green")
            else:
                # Stop streaming
                self.uav_stream_threads[uav_index - 1].stop()
                UAVs[uav_index]["status"]["streaming_status"] = False
                
                logger.log(f"UAV-{uav_index} streaming stopped", level="info")
                self.ui.btn_toggle_camera.setStyleSheet("background-color: red")
            
            # Update thread status
            self.uav_stream_threads[uav_index - 1].isRunning = UAVs[uav_index]["status"][
                "streaming_status"
            ]
            
        except Exception as e:
            logger.log(f"Camera toggle error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error toggling camera: {repr(e)}", 
                src_msg="uav_toggle_camera_callback",
                type_msg="Error"
            )

    async def uav_goto_callback(self, uav_index, page="settings", *args) -> None:
        """
        Command a specific UAV or all UAVs to go to GPS coordinates.
        
        This method retrieves GPS coordinates from the specified page's input fields
        and commands the UAV(s) to fly to those coordinates.
        
        Args:
            uav_index (int): The UAV to command (1-MAX_UAV_COUNT), or 0 for all UAVs
            page (str): Source page for GPS coordinates ("settings" or "overview")
            
        Returns:
            None

        Notes:
            - If the longitude or latitude values are empty, default values are used.
            - The coordinates are updated in the UI fields for both 'settings' and 'overview' pages.
            - If uav_index is 0, all UAVs will navigate to the specified point concurrently.
        """
        global UAVs
        
        try:
            # Get coordinates from the appropriate page
            longitude, latitude = self._get_coordinates_from_page(page, uav_index)
                
            # Ensure coordinates are valid
            if longitude is None or latitude is None:
                logger.log("Invalid coordinates for goto command", level="warning")
                self.popup_msg(
                    "Invalid coordinates for goto command",
                    src_msg="uav_goto_callback",
                    type_msg="Warning"
                )
                return
                
            # Sync coordinates between settings and overview pages
            self._sync_coordinates_between_pages(longitude, latitude)
            
            # Execute goto command for specific UAV or all UAVs
            if uav_index in range(1, MAX_UAV_COUNT + 1):
                # Skip if UAV is not connected or not allowed
                if not self._check_uav_connection(uav_index):
                    return
                    
                # Send the command
                self.update_terminal(
                    f"[INFO] Sent GOTO command to UAV {uav_index}: lat={latitude}, lon={longitude}"
                )
                await uav_fn_goto_location(
                    drone=UAVs[uav_index], latitude=latitude, longitude=longitude
                )
                
                # Update status
                UAVs[uav_index]["status"]["mode_status"] = "Going to position"
                self._update_uav_info_display(uav_index)
                
            else:
                # Command all UAVs to go to the same position
                goto_tasks = []
                for i in range(1, MAX_UAV_COUNT + 1):
                    if self._check_uav_connection(i):
                        self.update_terminal(
                            f"[INFO] Sent GOTO command to UAV {i}: lat={latitude}, lon={longitude}"
                        )
                        goto_tasks.append(
                            uav_fn_goto_location(
                                drone=UAVs[i], latitude=latitude, longitude=longitude
                            )
                        )
                        
                        # Update status
                        UAVs[i]["status"]["mode_status"] = "Going to position"
                        self._update_uav_info_display(i)
                        
                if goto_tasks:
                    await asyncio.gather(*goto_tasks)
                
        except Exception as e:
            logger.log(f"Goto error: {repr(e)}", level="error")
            self.popup_msg(
                f"Error in goto command: {repr(e)}",
                src_msg="uav_goto_callback",
                type_msg="Error"
            )

    def _get_coordinates_from_page(self, page, uav_index):
        """Get coordinates from the specified page with fallback to defaults."""
        global UAVs
        
        # Set default coordinates (offset by UAV index to avoid collisions)
        default_longitude = UAVs[uav_index]["init_params"]["longitude"] if uav_index > 0 else INIT_LON
        default_latitude = UAVs[uav_index]["init_params"]["latitude"] if uav_index > 0 else INIT_LAT
        
        # Get coordinates from the specified page
        if page == "settings":
            longitude_text = self.ui.lineEdit_sett_longitude.text().strip()
            latitude_text = self.ui.lineEdit_sett_latitude.text().strip()
        else:  # overview page
            longitude_text = self.ui.lineEdit_ovv_longitude.text().strip()
            latitude_text = self.ui.lineEdit_ovv_latitude.text().strip()
        
        # Parse coordinates with fallback to defaults
        try:
            longitude = float(longitude_text) if longitude_text else default_longitude
            latitude = float(latitude_text) if latitude_text else default_latitude
            return longitude, latitude
        except ValueError:
            logger.log(f"Invalid coordinate format: lon={longitude_text}, lat={latitude_text}", level="error")
            return None, None

    def _sync_coordinates_between_pages(self, longitude, latitude):
        """Synchronize coordinates between settings and overview pages."""
        # Format coordinates to ensure consistent display
        lon_str = f"{longitude:.8f}"
        lat_str = f"{latitude:.8f}"
        
        # Update both pages to maintain consistency
        self.ui.lineEdit_ovv_longitude.setText(lon_str)
        self.ui.lineEdit_ovv_latitude.setText(lat_str)
        self.ui.lineEdit_sett_longitude.setText(lon_str)
        self.ui.lineEdit_sett_latitude.setText(lat_str)

    def _update_uav_info_display(self, uav_index):
        """Update the information display for a UAV."""
        global UAVs
        
        self.uav_information_views[uav_index - 1].setText(
            self.template_information(uav_index, **UAVs[uav_index]["status"])
        )
        
    def set_connection_display(self, uav_index, uav_status):
        """
        Updates the connection status of a UAV in the UI.

        Args:
            uav_index (int): The index of the UAV to update.
            status (bool): The connection status of the UAV.

        Returns:
            None
        """
        global UAVs
        
        if uav_status["connection_status"]:
            self.uav_label_params[uav_index - 1].setStyleSheet("background-color: green")
        else:
            self.uav_label_params[uav_index - 1].setStyleSheet("background-color: red")

        self.uav_information_views[uav_index - 1].setText(
            self.template_information(uav_index, **uav_status)
        )

    # --------------------------<UAVs get status functions>-----------------------------
    async def uav_fn_get_status(self, uav_index, verbose=1) -> None:
        """
        Retrieve and update all status information for a UAV or all UAVs.
        
        This function fetches and updates position, mode, battery, arm status, GPS info,
        and flight parameters for the specified UAV. It can also handle retrieving status
        for all UAVs when uav_index is out of range.
        
        Args:
            uav_index (int): The UAV to get status for (1-MAX_UAV_COUNT), or out of range for all UAVs
            verbose (int): If 1, also display status text messages in the terminal
            
        Returns:
            None
        """
        global UAVs
        
        # Handle getting status for all UAVs
        if uav_index not in range(1, MAX_UAV_COUNT + 1):
            status_tasks = [
                self.uav_fn_get_status(i, verbose=verbose)
                for i in range(1, MAX_UAV_COUNT + 1)
                if UAVs[i]["connection_allow"]
            ]
            await asyncio.gather(*status_tasks)
            return
        
        # Skip if UAV is not connected and not allowed
        if not (UAVs[uav_index]["status"]["connection_status"] and UAVs[uav_index]["connection_allow"]):
            return
        
        try:
            # Create a list of status retrieval functions to run concurrently
            status_tasks = [
                self.uav_fn_get_position(uav_index),
                self.uav_fn_get_mode(uav_index),
                self.uav_fn_get_battery(uav_index),
                self.uav_fn_get_arm_status(uav_index),
                self.uav_fn_get_gps(uav_index),
                self.uav_fn_get_flight_info(uav_index, copy=False),
            ]
            
            # Add status text messages if verbose mode is enabled
            if verbose:
                status_tasks.append(self.uav_fn_print_status(uav_index))
            
            # Run all status tasks concurrently
            await asyncio.gather(*status_tasks)
            
        except Exception as e:
            logger.log(f"Failed to get status for UAV {uav_index}: {e}", level="error")
            UAVs[uav_index]["status"]["connection_status"] = False
            self.set_connection_display(uav_index, UAVs[uav_index]["status"])
            self.popup_msg(
                f"Error retrieving UAV {uav_index} status: {repr(e)}", 
                src_msg="uav_fn_get_status", 
                type_msg="error"
            )
        
    async def uav_fn_get_position(self, uav_index) -> None:
        """
        Retrieve and update position data for a UAV.
        
        This function gets the current altitude (relative and absolute) and geographic
        position (latitude and longitude) of the specified UAV.
        
        Args:
            uav_index (int): The UAV to get position for (1-MAX_UAV_COUNT)
            
        """
        global UAVs
        
        try:
            # Get a single position update
            async for position in UAVs[uav_index]["system"].telemetry.position():
                # Extract position data with appropriate precision
                alt_rel = round(position.relative_altitude_m, 12)
                alt_msl = round(position.absolute_altitude_m, 12)
                latitude = round(position.latitude_deg, 12)
                longitude = round(position.longitude_deg, 12)
                
                # Update the UAV status dictionary
                UAVs[uav_index]["status"]["altitude_status"] = [alt_rel, alt_msl]
                UAVs[uav_index]["status"]["position_status"] = [latitude, longitude]
                
                # Update the position in the current position log file
                self._update_position_log(uav_index, latitude, longitude)
                
                # Update the UI
                self._update_uav_info_display(uav_index)
                
                # show on map
                # self.show_drones(init=False)
                    
                # Only process one position update per call, comment out if you want to make it continuous
                # break
                
        except Exception as e:
            logger.log(f"Failed to get position for UAV {uav_index}: {e}", level="error")
                
        return
    
    def _update_position_log(self, uav_index, latitude, longitude):
        """Update the current position log file for the UAV."""
        global UAVs
        try:
            # position_file = f"{__current_path__}/logs/drone_current_pos/uav_{uav_index}.txt"
            # os.makedirs(os.path.dirname(position_file), exist_ok=True)
            position_file = drone_current_pos_files[uav_index - 1]
            
            if not os.path.exists(position_file):
                os.makedirs(os.path.dirname(position_file), exist_ok=True)
                
            with open(position_file, "w") as f:
                f.write(f"{latitude},{longitude}")
                
        except Exception as e:
            logger.log(f"Failed to update position log for UAV {uav_index}: {e}", level="warning")

    async def uav_fn_get_mode(self, uav_index) -> None:
        """
        Retrieve and update the flight mode status of a UAV.
        
        Args:
            uav_index (int): The UAV to get mode for (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Get a single flight mode update
            async for mode in UAVs[uav_index]["system"].telemetry.flight_mode():
                # Update the UAV status dictionary
                UAVs[uav_index]["status"]["mode_status"] = mode
                
                # Update the UI
                self._update_uav_info_display(uav_index)
                
                # Only process one position update per call, comment out if you want to make it continuous
                # break
                
        except Exception as e:
            logger.log(f"Failed to get flight mode for UAV {uav_index}: {e}", level="error")


    async def uav_fn_get_battery(self, uav_index) -> None:
        """
        Retrieve and update the battery status of a UAV.
        
        Args:
            uav_index (int): The UAV to get battery status for (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Get a single battery update
            async for battery in UAVs[uav_index]["system"].telemetry.battery():
                # Calculate and format battery percentage
                battery_percent = round(battery.remaining_percent * 100, 1)
                battery_status = f"{battery_percent}%"
                
                # Update the UAV status dictionary
                UAVs[uav_index]["status"]["battery_status"] = battery_status
                
                # Update the UI with critical warning if battery is low
                self._update_uav_info_display(uav_index)
                
                # Log warning if battery is low
                if battery_percent < 10:
                    logger.log(f"WARNING: UAV {uav_index} battery at {battery_percent}%", level="warning")
                    self.update_terminal(f"[WARNING] UAV {uav_index} battery at {battery_percent}%", uav_index)
                    break
                # Only process one battery update per call
                # break
                
        except Exception as e:
            logger.log(f"Failed to get battery status for UAV {uav_index}: {e}", level="error")


    async def uav_fn_get_arm_status(self, uav_index) -> None:
        """
        Retrieve and update the arming status of a UAV.
        
        Args:
            uav_index (int): The UAV to get arm status for (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Get a single arm status update
            async for armed in UAVs[uav_index]["system"].telemetry.armed():
                # Convert boolean to status string
                arm_status = "ARMED" if armed else "DISARMED"
                
                # Update the UAV status dictionary
                UAVs[uav_index]["status"]["arming_status"] = arm_status
                
                # Update the UI
                self._update_uav_info_display(uav_index)
                
                # Only process one arm status update per call
                # break
                
        except Exception as e:
            logger.log(f"Failed to get arm status for UAV {uav_index}: {e}", level="error")

    async def uav_fn_get_gps(self, uav_index) -> None:
        """
        Retrieve and update GPS information for a UAV.
        
        Args:
            uav_index (int): The UAV to get GPS info for (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Get a single GPS update
            async for gps in UAVs[uav_index]["system"].telemetry.gps_info():
                # Get GPS fix type
                gps_status = gps.fix_type
                
                # Update the UAV status dictionary
                UAVs[uav_index]["status"]["gps_status"] = gps_status
                
                # Update the UI
                self._update_uav_info_display(uav_index)
                
                # Log warning if GPS fix is poor
                if gps_status.value < 3:  # Less than 3D fix
                    logger.log(f"WARNING: UAV {uav_index} has poor GPS fix: {gps_status}", level="warning")
                    self.update_terminal(f"[WARNING] UAV {uav_index} has poor GPS fix: {gps_status}", uav_index)
                
                # Only process one GPS update per call
                # break
                
        except Exception as e:
            logger.log(f"Failed to get GPS info for UAV {uav_index}: {e}", level="error")

    async def uav_fn_get_flight_info(self, uav_index, copy=False) -> None:
        """
        Retrieve and update flight parameters for a UAV.
        
        This function gets the current flight parameters from the UAV and updates
        the parameter display fields in the UI. If 'copy' is True, it also copies 
        the values to the parameter input fields.
        
        Args:
            uav_index (int): The UAV to get parameters for (1-MAX_UAV_COUNT)
            copy (bool): If True, copy parameters to input fields
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Get parameters from the UAV
            parameters = await uav_fn_get_params(
                drone=UAVs[uav_index],
                list_params=displayed_parameter_list,
            )
            
            # Update parameter display fields
            for i, (param_name, value) in enumerate(parameters.items()):
                # Format the value to one decimal place
                formatted_value = str(round(value, 1))
                
                # Update the display field
                self.uav_param_displays[uav_index - 1].children()[i + 1].setText(formatted_value)
                
                # If requested, also copy to the input field
                if copy:
                    self.uav_param_sets[uav_index - 1].children()[i + 1].setText(formatted_value)
                    
        except Exception as e:
            logger.log(f"Failed to get flight parameters for UAV {uav_index}: {e}", level="error")
            self.popup_msg(
                f"Error retrieving flight parameters: {repr(e)}", 
                src_msg="uav_fn_get_flight_info", 
                type_msg="error"
            )

    async def uav_fn_set_flight_info(self, uav_index) -> None:
        """
        Set flight parameters for a UAV.
        
        This function gets parameter values from the input fields, validates them,
        and sends them to the UAV. It then refreshes the parameter display.
        
        Args:
            uav_index (int): The UAV to set parameters for (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        try:
            # Initialize parameters dictionary
            parameters = {}
            
            # Get widgets containing current and new values
            input_widgets = self.uav_param_sets[uav_index - 1].children()[1:-1]
            display_widgets = self.uav_param_displays[uav_index - 1].children()[1:-1]
            
            # Populate parameters from input fields, falling back to current values if empty
            for i, (input_widget, display_widget) in enumerate(zip(input_widgets, display_widgets)):
                param_name = displayed_parameter_list[i]
                input_text = input_widget.text()
                
                if not input_text:
                    # Use current value if input is empty
                    parameters[param_name] = float(display_widget.text())
                else:
                    try:
                        # Validate and convert input to float
                        parameters[param_name] = float(input_text)
                    except ValueError:
                        # Handle invalid input
                        logger.log(f"Invalid value for parameter {param_name}: {input_text}", level="warning")
                        self.popup_msg(
                            f"Invalid value for {param_name}: {input_text}", 
                            src_msg="uav_fn_set_flight_info", 
                            type_msg="Warning"
                        )
                        # Use current value instead
                        parameters[param_name] = float(display_widget.text())
            
            # Send parameters to the UAV and save to file
            await uav_fn_set_params(
                drone=UAVs[uav_index],
                parameters=parameters,
                param_file=parameter_data_files[uav_index - 1],
            )
            
            # Refresh parameter display
            await self.uav_fn_get_flight_info(uav_index=uav_index, copy=False)
            
            # Log and display success message
            logger.log(f"Updated flight parameters for UAV {uav_index}", level="info")
            self.update_terminal(f"[INFO] Updated flight parameters for UAV {uav_index}")
            
        except Exception as e:
            logger.log(f"Failed to set flight parameters for UAV {uav_index}: {e}", level="error")
            self.popup_msg(
                f"Error setting flight parameters: {repr(e)}", 
                src_msg="uav_fn_set_flight_info", 
                type_msg="Error"
            )

    async def uav_fn_print_status(self, uav_index) -> None:
        """
        Display status text messages from a UAV in the terminal.
        
        Args:
            uav_index (int): The UAV to get status messages from (1-MAX_UAV_COUNT)
            
        Returns:
            None
        """
        global UAVs
        
        # Skip if UAV is not connected or not allowed
        if not self._check_uav_connection(uav_index):
            return
        
        try:
            # Get and display status text messages
            async for status in UAVs[uav_index]["system"].telemetry.status_text():
                # Format the status message
                status_text = f"> {status.type} - {status.text}"
                
                # Display in the terminal
                self.update_terminal(status_text, uav_index)
                
                # Log to file based on severity
                if status.type.name in ["ERROR", "CRITICAL"]:
                    logger.log(f"UAV {uav_index}: {status.text}", level="error")
                elif status.type.name == "WARNING":
                    logger.log(f"UAV {uav_index}: {status.text}", level="warning")
                else:
                    logger.log(f"UAV {uav_index}: {status.text}", level="debug")
                    
        except Exception as e:
            logger.log(f"Failed to print status for UAV {uav_index}: {e}", level="error")

    # -----------------------------< UAVs streaming functions >-----------------------------
    @pyqtSlot(np.ndarray, np.ndarray, list)
    def stream_on_uav_screen(self, frame=None, annotated_frame=None, results=None) -> None:
        """
        Display video stream on the UAV screen with optional object detection annotations.
        
        This method processes video frames for display in the UAV interface. It handles raw 
        or annotated frames with detection results, manages frame rate throttling, and exports 
        detection data when targets are found.
        
        Args:
            frame (np.ndarray): The original video frame without annotations
            annotated_frame (np.ndarray): The frame with detection annotations
            results (list): Contains [uav_index, current_fps, detected_results] where:
                            - uav_index: The UAV identifier
                            - current_fps: Current frames per second
                            - detected_results: Detection results including track IDs and object data
        
        Returns:
            None

        Notes:
            - The method only processes frames if UAV connection is allowed and streaming is enabled
            - Frame rate is limited according to DEFAULT_STREAM_FPS
            - When detection is enabled and a person is detected, the frame is saved and GPS coordinates
            are exported to logs
        """

        global UAVs
        if not results:
            logger.log("Received empty results in stream handler", level="warning")
            return
            
        # Unpack the results
        uav_index, current_fps, detected_results = results
        uav_index = int(uav_index)
        
        # Skip processing if UAV is not eligible for streaming
        if not self._can_stream(uav_index):
            return
            
        try:
            # Apply frame rate limiting
            if not self._should_process_frame(uav_index, current_fps):
                return
                
            # Select the appropriate frame to display
            streaming_frame = self._select_frame_type(uav_index, frame, annotated_frame)
            
            # Display the frame
            self.update_uav_screen_view(
                uav_index, streaming_frame, screen_name=DEFAULT_STREAM_SCREEN
            )
            
            # Process detection results if available and detection is enabled
            if UAVs[uav_index]["detection_enable"] and detected_results:
                self._process_detection_results(uav_index, annotated_frame, detected_results)
                
        except Exception as e:
            # Update status and show error message
            UAVs[uav_index]["status"]["streaming_status"] = False
            logger.log(f"Stream display error for UAV {uav_index}: {repr(e)}", level="error")
            self.popup_msg(
                f"Stream display error: {repr(e)}",
                src_msg="stream_on_uav_screen",
                type_msg="error",
            )
            
            
    def _check_uav_connection(self, uav_index, strictly=True):
        """Check if a UAV is connected and allowed to receive commands."""
        if strictly:
            return (UAVs[uav_index]["status"]["connection_status"] and 
                    UAVs[uav_index]["connection_allow"])
        else:
            return (UAVs[uav_index]["status"]["connection_status"] or
                    UAVs[uav_index]["connection_allow"])
            
    def _can_stream(self, uav_index):
        """Check if UAV is eligible for stream display."""
        return (
            self._check_uav_connection(uav_index=uav_index, strictly=False) and 
            UAVs[uav_index]["streaming_enable"]
        )

    def _should_process_frame(self, uav_index, current_fps):
        """Apply frame rate limiting to avoid overloading the UI."""
        # Calculate the frame skip rate to achieve target FPS
        max_frame_cnt = max(1, current_fps // DEFAULT_STREAM_FPS)
        
        # Increment the frame counter for this UAV
        self.uav_stream_frame_cnt[uav_index - 1] += 1
        
        # Process frame if it's time to display based on our rate limiting
        return self.uav_stream_frame_cnt[uav_index - 1] % max_frame_cnt == 0

    def _select_frame_type(self, uav_index, frame, annotated_frame):
        """Select which frame to display based on detection settings."""
        # Use annotated frame if detection is enabled, otherwise use raw frame
        return annotated_frame if UAVs[uav_index]["detection_enable"] else frame

    def _process_detection_results(self, uav_index, annotated_frame, detected_results):
        """Process object detection results and handle detected targets."""
        global UAVs
        
        if len(detected_results) != 2:
            return
            
        track_ids, objects = detected_results
        
        for track_id, obj in zip(track_ids, objects):
            # Skip if not a detected person
            if not obj["detected"] or obj["class"] != "person":
                continue
                
            # Get UAV position and frame information
            frame_shape = annotated_frame.shape
            detected_pos = (obj["x"], obj["y"])
            
            # Get current GPS coordinates
            # with open(drone_current_pos_files[uav_index - 1], "r") as f:
            #     gps_data = f.read()
            #     uav_lat, uav_long = map(float, gps_data.split(","))
                
            uav_lat, uav_long = UAVs[uav_index]["status"]["position_status"]
            uav_alt = UAVs[uav_index]["status"]["altitude_status"][0]
            uav_gps = [uav_lat, uav_long, uav_alt]
            
            # Save the detection frame
            self._save_detection_image(uav_index, track_id, annotated_frame)
            
            # Log detection to terminal
            self._log_detection(uav_index, obj["class"], detected_pos, frame_shape, uav_gps)
            
            # Export detection to GPS log
            export_points_to_gps_log(
                uav_index=uav_index,
                detected_pos=detected_pos,
                frame_shape=frame_shape,
                uav_gps=uav_gps,
            )
            
            # Disable detection feature after finding a target
            UAVs[uav_index]["detection_enable"] = False
            
            # Only process the first detected person
            break

    def _save_detection_image(self, uav_index, track_id, frame):
        """Save a detection image to the logs directory."""
        image_path = f"{__current_path__}/logs/images/UAV{uav_index}_locked_target_{track_id}.png"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        cv2.imwrite(image_path, frame)
        logger.log(f"Saved detection image to {image_path}", level="info")

    def _log_detection(self, uav_index, class_name, detected_pos, frame_shape, uav_gps):
        """Log detection information to the terminal."""
        global UAVs
        
        detection_msg = (
            f"UAV-{uav_index} at GPS ({uav_gps[0]}, {uav_gps[1]}, {uav_gps[2]}m) "
            f"detected {class_name} at X: {detected_pos[0]:.1f} Y: {detected_pos[1]:.1f} "
            f"with frame size: {frame_shape[1]}x{frame_shape[0]}"
        )
        self.update_terminal(detection_msg, 0)
        logger.log(detection_msg, level="info")
        
    # ------------------------------------< Rescue UAV 6 >-----------------------------
    # ? developing ...
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
        # TODO: check battery level here
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
        
        try:
            # do the rescue mission loop
            # 1. check if the rescue position is available
            # 2. get the detected UAVs
            # 3. do the rescue mission

            while True:
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

                # NOTE: you can implement your own logic here
                # get the detected UAVs
                detected_uav_list = []
                for rescue_filepath in rescue_filepaths:
                    uav_index = int(str(Path(rescue_filepath).stem).split("_")[-1])
                    print(f"Detected UAV: {uav_index}")
                    detected_uav_list.append(UAVs[uav_index])
                
                # get the rescue filepath
                
                logger.log(
                    f"Found {len(rescue_filepaths)} rescue files",
                    level="info",
                )
                rescue_filepath = select_mission_plan(rescue_filepaths)
                logger.log(
                    f"Selected rescue file: {rescue_filepath}",
                    level="info",
                )
                
                # 
                logger.log("Rescue mission started...", level="info")
                               
                logger.log(
                    f"UAV-{RESCUE_UAV_INDEX} -- Takeoff completed, ready to start rescue mission", level="info"
                )

                # get initial position
                async for position in UAVs[RESCUE_UAV_INDEX]["system"].telemetry.position():
                    UAVs[RESCUE_UAV_INDEX]["init_params"]["latitude"] = round(position.latitude_deg, 12)
                    UAVs[RESCUE_UAV_INDEX]["init_params"]["longitude"] = round(position.longitude_deg, 12)
                    break
                
                # 2 UAV Rescue do the rescue mission and the detected drones goes into suspend mode
                UAVs[RESCUE_UAV_INDEX]["status"]["on_mission"] = True
                await asyncio.gather(
                    uav_suspend_missions(drones=detected_uav_list, suspend_time=30),
                    uav_rescue_process(
                        drone=UAVs[RESCUE_UAV_INDEX], rescue_filepath=rescue_filepath
                    ),
                )
                UAVs[RESCUE_UAV_INDEX]["status"]["on_mission"] = False
                UAVs[RESCUE_UAV_INDEX]["rescue_first_time"] = False
                
                # 3 remove the rescue file
                if os.path.exists(rescue_filepath):
                    os.remove(rescue_filepath)  # remove the rescue file
                    logger.log(f"Rescue file {rescue_filepath} removed", level="info")
                
                # 4 remove the detected UAVs from the list
                # self.detected_uav_list.remove(uav_index)
                # self.detected_uav_list = []
                break  # remove this line if you want to do the rescue mission continuously

            logger.log(f"Rescue mission completed", level="info")
            # start rescue mission again
            await self.uav_fn_rescue()
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
