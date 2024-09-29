import os
import sys
import time
from pathlib import Path

import cv2
from drone import *
from imutils.video import FPS
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
)

from UI.interface_uav import *
from utils.map_utils import *

MAX_UAV_COUNT = 6

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
    1: {"uav": Drone("uav1", port=50060)},
    2: {"uav": Drone("uav2", port=50061)},
    3: {"uav": Drone("uav3", port=50062)},
    4: {"uav": Drone("uav4", port=50063)},
    5: {"uav": Drone("uav5", port=50064)},
    6: {"uav": Drone("uav6", port=50065)},
}


def convert_cv2qt(cv_img, size=(640, 360)):
    """Convert cv image to qt image to display on gui

    Args:
        cv_img (ndarray): BGR image

    Returns:
        image: RGB image with qt format
    """
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(
        rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
    )
    p = convert_to_Qt_format.scaled(*size, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


class App(QMainWindow):
    def __init__(self, model=None) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.active_tab_index = 0
        self.active_stack_index = 0

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

        self.uav_update_commands = [
            self.ui.lineEdit_infor_uav_1,
            self.ui.lineEdit_infor_uav_2,
            self.ui.lineEdit_infor_uav_3,
            self.ui.lineEdit_infor_uav_4,
            self.ui.lineEdit_infor_uav_5,
            self.ui.lineEdit_infor_uav_6,
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

        #
        self.init_application()

    def init_application(self):
        # reset path for assets and videos
        basePath = Path(__file__)
        basePath = basePath.resolve().parents[0].parents[0]

        # logo
        self.ui.page_name.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logo1.png"))
        self.ui.page_name.setScaledContents(True)
        self.ui.page_name_2.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logo1.png"))
        self.ui.page_name_2.setScaledContents(True)
        self.ui.logo2_2.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logoUET.png"))
        self.ui.logo2_2.setScaledContents(True)
        self.ui.logo2.setPixmap(QtGui.QPixmap(f"{basePath}/assets/icons/logoUET.png"))
        self.ui.logo2.setScaledContents(True)

        # screen view
        for screen in self.uav_general_screen_views:
            screen.setPixmap(QtGui.QPixmap(f"{basePath}/assets/pictures/nosignal.jpg"))
            screen.setScaledContents(True)
        for screen in self.uav_stream_screen_views:
            screen.setPixmap(QtGui.QPixmap(f"{basePath}/assets/pictures/no_signal2.jpg"))
            screen.setScaledContents(True)
        for screen in self.uav_ovv_screen_views:
            screen.setPixmap(QtGui.QPixmap(f"{basePath}/assets/pictures/nosignal.jpg"))
            screen.setScaledContents(True)

        # map
        self.ui.MapWebView.setUrl(QtCore.QUrl(f"file://{basePath}/assets/map.html"))

        self.ui.Overview_map_view.setUrl(QtCore.QUrl(f"file://{basePath}/assets/map.html"))

        # set default tab and stack index
        self.ui.stackedWidget.setCurrentIndex(self.active_stack_index)
        self.ui.tabWidget.setCurrentIndex(self.active_tab_index)

        self.map_menuBar_clicked()

        self.map_tab_clicked()

        self.map_button_event()

        self.map_uav_to_ui()

        #
        self.map = MapEngine(self.ui.MapWebView)

        self.map.mapMovedCallback = self.onMapMoved
        self.map.mapClickedCallback = self.onMapLClick
        self.map.mapDoubleClickedCallback = self.onMapDClick
        self.map.mapRightClickedCallback = self.onMapRClick

        # self.map.markerMovedCallback = self.onMarkerMoved
        # self.map.markerClickedCallback = self.onMarkerLClick
        # self.map.markerDoubleClickedCallback = self.onMarkerDClick
        # self.map.markerRightClickedCallback = self.onMarkerRClick

    # //-/////////////////////////////////////////////////////////////
    # //-/////////////////////////////////////////////////////////////
    def template_information(
        self,
        uav_index,
        connection_status=False,
        arming_status="No information",
        battery_status="No information",
        gps_status="No information",
        mode_status="No information",
        speed_status="No information",
        altitude_status=["No information", "No information"],
        position_status=["No information", "No information"],
    ):
        """Template for information view

        Args:
            uav_index (int): index of UAV
        """
        msg = f"""===========================================
            UAV {uav_index} Information\n
            - Connection:\t{connection_status}\n
            - Arming:\t{arming_status}\n
            - Battery:\t{battery_status}\n
            - GPS (FIXED):\t{gps_status}\n
            - Mode:\t{mode_status}\n
            - Speed:\t{speed_status}\n
            - Altitude (Rel):\t{altitude_status[0]}m\n
            - Altitude (Abs):\t{altitude_status[1]}m\n
            - Position: 
                Longitude:\t{position_status[0]}
                Latitude:\t{position_status[1]}
        ============================================
        """
        return msg

    def map_uav_to_ui(self):
        """
        This function maps each UAV to its corresponding UI components.

        Parameters:
        None

        Returns:
        None
        """
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

    def map_menuBar_clicked(self):
        # setup tabs menubar actions
        self.ui.actionUAV_1_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav1")
        )
        self.ui.actionUAV_2_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav2")
        )
        self.ui.actionUAV_3_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav3")
        )
        self.ui.actionUAV_4_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav4")
        )
        self.ui.actionUAV_5_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav5")
        )
        self.ui.actionUAV_6_view.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "uav6")
        )

        self.ui.actionOverview.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "all")
        )
        self.ui.actionScreen_10_Settings.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "settings")
        )
        self.ui.actionScreen_7_Rescue_map.triggered.connect(
            lambda: self.switch_with_menuBar("map page", "all")
        )
        self.ui.actionScreen_11_Overview.triggered.connect(
            lambda: self.switch_with_menuBar("main page", "overview")
        )

    def map_tab_clicked(self):
        self.ui.tabWidget.tabBarClicked.connect(self.switch_with_tabBar)

    def switch_with_tabBar(self, index):
        self.active_tab_index = index
        self.active_stack_index = self.ui.stackedWidget.currentIndex()

    def switch_with_menuBar(self, stack_name, tab_name):
        self.ui.stackedWidget.setCurrentIndex(stackedWidget_indexes[stack_name])
        self.ui.tabWidget.setCurrentIndex(tabWidget_indexes[tab_name])
        self.active_tab_index = self.ui.tabWidget.currentIndex()
        self.active_stack_index = self.ui.stackedWidget.currentIndex()

    def map_button_event(self):
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
            lambda: asyncio.create_task(self.uav_fn_pause(self.active_tab_index))
        )

        self.ui.btn_connect.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_connect(self.active_tab_index))
        )

        self.ui.btn_return.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_return(self.active_tab_index))
        )

        self.ui.btn_mission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_mission(self.active_tab_index))
        )

        self.ui.btn_pushMission.clicked.connect(
            lambda: asyncio.create_task(self.uav_fn_pushMission(self.active_tab_index))
        )

    async def uav_fn_arm(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent ARM command to UAV {uav_index}"
            info = self.template_information(uav_index, arming_status="ARMED")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].arming()
            #
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)

        pass

    async def uav_fn_disarm(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent DISARM command to UAV {uav_index}"
            info = self.template_information(uav_index, arming_status="DISARMED")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].disarm()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_takeoff(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent TAKEOFF command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Take-off")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].takeOff()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_return(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent RETURN command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Return")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].returnToLaunch()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_landing(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent LANDING command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Landing")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].land()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_connect(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent CONNECT command to UAV {uav_index}"
            info = self.template_information(uav_index, connection_status="Connected")
            UAVs[uav_index]["uav"].connect()
            # await asyncio.sleep(1)
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_pause(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent PAUSE command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Pause")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].pauseMission()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_mission(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent MISSION command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Mission")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].performMission()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_pushMission(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent PUSH MISSION command to UAV {uav_index}"
            info = self.template_information(uav_index, mode_status="Push Mission")
            await asyncio.sleep(1)
            UAVs[uav_index]["uav"].uploadMission()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)
        pass

    async def uav_fn_openClose(self, uav_index):
        if uav_index != 0:
            msg = f"[INFO] Sent OPEN/CLOSE command to UAV {uav_index}"
            info = self.template_information(
                uav_index,
                mode_status="Open" if UAVs[uav_index]["uav"].openClose_status else "Close",
            )
            await asyncio.sleep(1)
            # UAVs[uav_index]['uav'].openClose()
            UAVs[uav_index]["information_view"].setText(info)
            self.update_terminal(msg)

    def update_terminal(self, text):
        self.ui.mainTerminal.setFocus()
        self.ui.mainTerminal.moveCursor(self.ui.mainTerminal.textCursor().End)
        self.ui.mainTerminal.appendPlainText(text)

    # map handling functions

    def onMapMoved(self, latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(self, latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(self, latitude, longitude):
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude):
        print("DClick on ", latitude, longitude)


def run():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = App()
    MainWindow.show()
    with loop:
        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
