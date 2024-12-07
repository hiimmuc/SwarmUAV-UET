# cspell: ignore asyncqt
import asyncio
import sys

from asyncqt import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from config.interface_config import *
from config.stream_config import *
from config.uav_config import *
from Qt.interface_uav import *
from utils.logger import *
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
logger = Logger()

# cSpell:ignore uavs pixmap


class Interface(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # starting stack and tab index
        self.active_tab_index = 0
        self.active_stack_index = 0

        # UAVs UI components
        self.uav_tabs = [
            self.ui.actionUAV_1_view,
            self.ui.actionUAV_2_view,
            self.ui.actionUAV_3_view,
            self.ui.actionUAV_4_view,
            self.ui.actionUAV_5_view,
            self.ui.actionUAV_6_view,
        ]  # tabs in stacked widget

        self.uav_stream_screen_views = [
            self.ui.stream_screen_1,
            self.ui.stream_screen_2,
            self.ui.stream_screen_3,
            self.ui.stream_screen_4,
            self.ui.stream_screen_5,
            self.ui.stream_screen_6,
        ]  # stream screen views on page 1-6

        self.uav_general_screen_views = [
            self.ui.general_screen_uav_1,
            self.ui.general_screen_uav_2,
            self.ui.general_screen_uav_3,
            self.ui.general_screen_uav_4,
            self.ui.general_screen_uav_5,
            self.ui.general_screen_uav_6,
        ]  # general screen views on the general page

        self.uav_ovv_screen_views = [
            self.ui.ovv_screen_uav_1,
            self.ui.ovv_screen_uav_2,
            self.ui.ovv_screen_uav_3,
            self.ui.ovv_screen_uav_4,
            self.ui.ovv_screen_uav_5,
            self.ui.ovv_screen_uav_6,
        ]  # ovv screen views on the overview page

        self.uav_information_views = [
            self.ui.information_uav_1,
            self.ui.information_uav_2,
            self.ui.information_uav_3,
            self.ui.information_uav_4,
            self.ui.information_uav_5,
            self.ui.information_uav_6,
        ]  # information views page 1-6

        self.uav_status_views = [
            self.ui.status_uav_1,
            self.ui.status_uav_2,
            self.ui.status_uav_3,
            self.ui.status_uav_4,
            self.ui.status_uav_5,
            self.ui.status_uav_6,
        ]  # status views page 1-6

        self.uav_update_commands = [
            self.ui.cmdLine_uav_1,
            self.ui.cmdLine_uav_2,
            self.ui.cmdLine_uav_3,
            self.ui.cmdLine_uav_4,
            self.ui.cmdLine_uav_5,
            self.ui.cmdLine_uav_6,
        ]  # command line page 1-6 to enter commands

        self.uav_label_params = [
            self.ui.label_param_uav_1,
            self.ui.label_param_uav_2,
            self.ui.label_param_uav_3,
            self.ui.label_param_uav_4,
            self.ui.label_param_uav_5,
            self.ui.label_param_uav_6,
        ]  # label params page 1-6

        self.uav_param_displays = [
            self.ui.param_current_uav_1,
            self.ui.param_current_uav_2,
            self.ui.param_current_uav_3,
            self.ui.param_current_uav_4,
            self.ui.param_current_uav_5,
            self.ui.param_current_uav_6,
        ]  # param display page 1-6

        self.uav_param_sets = [
            self.ui.param_set_uav_1,
            self.ui.param_set_uav_2,
            self.ui.param_set_uav_3,
            self.ui.param_set_uav_4,
            self.ui.param_set_uav_5,
            self.ui.param_set_uav_6,
        ]  # param set page 1-6

        self.uav_set_param_buttons = [
            self.ui.btn_param_set_uav_1,
            self.ui.btn_param_set_uav_2,
            self.ui.btn_param_set_uav_3,
            self.ui.btn_param_set_uav_4,
            self.ui.btn_param_set_uav_5,
            self.ui.btn_param_set_uav_6,
        ]  # set param buttons page 1-6

        self.uav_get_param_buttons = [
            self.ui.btn_param_dis_uav_1,
            self.ui.btn_param_dis_uav_2,
            self.ui.btn_param_dis_uav_3,
            self.ui.btn_param_dis_uav_4,
            self.ui.btn_param_dis_uav_5,
            self.ui.btn_param_dis_uav_6,
        ]  # get param buttons page 1-6

        self.uav_sett_goTo_buttons = [
            self.ui.btn_sett_goto_uav_all,
            self.ui.btn_sett_goto_uav_1,
            self.ui.btn_sett_goto_uav_2,
            self.ui.btn_sett_goto_uav_3,
            self.ui.btn_sett_goto_uav_4,
            self.ui.btn_sett_goto_uav_5,
            self.ui.btn_sett_goto_uav_6,
        ]  # go to buttons on page settings

        self.uav_ovv_goTo_buttons = [
            self.ui.btn_ovv_goto_uav_all,
            self.ui.btn_ovv_goto_uav_1,
            self.ui.btn_ovv_goto_uav_2,
            self.ui.btn_ovv_goto_uav_3,
            self.ui.btn_ovv_goto_uav_4,
            self.ui.btn_ovv_goto_uav_5,
            self.ui.btn_ovv_goto_uav_6,
        ]  # go to buttons on page overview

        self.sett_checkBox_active_lists = [
            self.ui.sett_checkBox_active_uav_1,
            self.ui.sett_checkBox_active_uav_2,
            self.ui.sett_checkBox_active_uav_3,
            self.ui.sett_checkBox_active_uav_4,
            self.ui.sett_checkBox_active_uav_5,
            self.ui.sett_checkBox_active_uav_6,
        ]  # active checkboxes on page settings

        self.sett_checkBox_detect_lists = [
            self.ui.sett_checkBox_detect_uav_1,
            self.ui.sett_checkBox_detect_uav_2,
            self.ui.sett_checkBox_detect_uav_3,
            self.ui.sett_checkBox_detect_uav_4,
            self.ui.sett_checkBox_detect_uav_5,
            self.ui.sett_checkBox_detect_uav_6,
        ]  # detect checkboxes on page settings

        self.ovv_checkBox_detect_lists = [
            self.ui.ovv_checkBox_detect_uav_1,
            self.ui.ovv_checkBox_detect_uav_2,
            self.ui.ovv_checkBox_detect_uav_3,
            self.ui.ovv_checkBox_detect_uav_4,
            self.ui.ovv_checkBox_detect_uav_5,
            self.ui.ovv_checkBox_detect_uav_6,
        ]  # detect checkboxes on page overview

        self._init_interface()

    def _init_interface(self) -> None:
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

        # set app icon
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(app_icon_path)))

        # set button icons
        self.ui.btn_arm.setIcon(QtGui.QIcon(QtGui.QPixmap(arm_icon_path)))
        self.ui.btn_disarm.setIcon(QtGui.QIcon(QtGui.QPixmap(disarm_icon_path)))
        self.ui.btn_open_close.setIcon(QtGui.QIcon(QtGui.QPixmap(open_close_icon_path)))
        self.ui.btn_landing.setIcon(QtGui.QIcon(QtGui.QPixmap(landing_icon_path)))
        self.ui.btn_take_off.setIcon(QtGui.QIcon(QtGui.QPixmap(takeoff_icon_path)))
        self.ui.btn_pause_resume.setIcon(QtGui.QIcon(QtGui.QPixmap(pause_icon_path)))
        self.ui.btn_connect.setIcon(QtGui.QIcon(QtGui.QPixmap(connect_icon_path)))
        self.ui.btn_rtl.setIcon(QtGui.QIcon(QtGui.QPixmap(rtl_icon_path)))
        self.ui.btn_return.setIcon(QtGui.QIcon(QtGui.QPixmap(return_icon_path)))
        self.ui.btn_mission.setIcon(QtGui.QIcon(QtGui.QPixmap(mission_icon_path)))
        self.ui.btn_push_mission.setIcon(QtGui.QIcon(QtGui.QPixmap(push_mission_icon_path)))
        self.ui.btn_toggle_camera.setIcon(QtGui.QIcon(QtGui.QPixmap(toggle_icon_path)))

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

        # set default tab and stack index
        self.ui.stackedWidget.setCurrentIndex(self.active_stack_index)
        self.ui.tabWidget.setCurrentIndex(self.active_tab_index)

        # map events
        self._menu_bar_clicked_event()

        self._tab_clicked_event()

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
        try:
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
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(repr(e), src_msg="_menu_bar_clicked_event", type_msg="error")

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
        try:
            self.ui.stackedWidget.setCurrentIndex(stackedWidget_indexes[stack_name])
            self.ui.tabWidget.setCurrentIndex(tabWidget_indexes[tab_name])

            self.active_tab_index = self.ui.tabWidget.currentIndex()
            self.active_stack_index = self.ui.stackedWidget.currentIndex()
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(repr(e), src_msg="_switch_layout", type_msg="error")

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
                f"{'-----Rel:': <20}{altitude_status[0] : ^16}m".strip(),
                f"{'-----MSL:': <20}{altitude_status[1] : ^16}m".strip(),
                f"{'- Position:': <20}".strip(),
                f"{'-----Latitude:': <20}{position_status[0] : ^16}".strip(),
                f"{'-----Longitude:': <20}{position_status[1] : ^16}".strip(),
                "================================",
            ]
        )
        return _translate("MainWindow", msg)

    def update_terminal(self, text, uav_index=0) -> None:
        """
        Updates the terminal with the provided text.

        Parameters:
        text (str): The text to append to the terminal.
        uav_index (int, optional): The index of the UAV terminal to update.Defaults to 0, which updates the main terminal.

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

    def update_uav_screen_view(self, uav_index, frame=None, screen_name="all") -> None:
        """
        Starts streaming video from the specified UAV to the screen view.

        Args:
            uav_index (int): The index of the UAV to start streaming video from.

        Returns:
            None
        """
        screen_views = {
            "general_screen": self.uav_general_screen_views[uav_index - 1],
            "ovv_screen": self.uav_ovv_screen_views[uav_index - 1],
            "stream_screen": self.uav_stream_screen_views[uav_index - 1],
        }

        try:
            if screen_name != "all":
                if frame is None:  # show pause image
                    frame = cv2.imread(pause_img_paths[screen_name])

                width, height = screen_sizes[screen_name]
                screen_views[screen_name].setPixmap(convert_cv2qt(frame, size=(width, height)))
            else:  # all types of screen
                screen_names = ["general_screen", "ovv_screen", "stream_screen"]
                for name in screen_names:
                    self.update_uav_screen_view(uav_index, frame, screen_name=name)
        except Exception as e:
            logger.log(repr(e), level="error")

    def popup_msg(self, msg, src_msg="", type_msg="error"):
        """Create popup window to the ui

        Args:
            msg(str): message you want to show to the popup window
            src_msg(str, optional): source of the message. Defaults to ''.
            type_msg(str, optional): type of popup. Available: warning, error, information. Defaults to 'error'.
        """
        try:
            logger.log(f"From: {src_msg}\n[!] Details: {msg}", level=type_msg.lower())
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
        except Exception as e:
            print("-> From: popup_msg", e)


# ------------------------------------< Base Application Class >-----------------------------
def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Oxygen")  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = Interface()
    MainWindow.show()

    with loop:
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
