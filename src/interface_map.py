# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

# user-defined modules
from config import *
from interface_base import *
from UI.interface_uav import *
from utils.drone_utils import *
from utils.map_utils import *
from utils.qt_utils import *


class Map(Interface):
    def __init__(self):
        Interface.__init__(self)
        self._init_map()

    def _init_map(self):
        # map URL
        # file:///.../SwarmUAV-UET/assets/map.html
        self.ui.MapWebView.setUrl(QtCore.QUrl(map_html_path))
        # map engine
        self.map = MapEngine(self.ui.MapWebView)
        self.map.mapMovedCallback = self.onMapMoved
        self.map.mapClickedCallback = self.onMapLClick
        self.map.mapDoubleClickedCallback = self.onMapDClick
        self.map.mapRightClickedCallback = self.onMapRClick
        self.map.mapGeojsonCallback = self.onMapGeojson
        # Ovv map only for seeing
        self.map_data = load_map()
        # self.ui.MapWebView.setHtml(self.map_data)
        self.ui.Overview_map_view.setHtml(self.map_data)
        # self.ui.Overview_map_view.setUrl(QtCore.QUrl(map_html_path))
        self.ovv_map = MapEngine(self.ui.Overview_map_view)

    # -----------------------------< custom map functions >-----------------------------
    def onMarkerMoved(self, key, latitude, longitude) -> None:
        print("Moved!!", key, latitude, longitude)

    def onMarkerRClick(self, key, latitude, longitude) -> None:
        print("RClick on ", key, latitude, longitude)

    def onMarkerLClick(self, key, latitude, longitude) -> None:
        print("LClick on ", key, latitude, longitude)

    def onMarkerDClick(self, key, latitude, longitude) -> None:
        print("DClick on ", key, latitude, longitude)

    def onMapMoved(self, latitude, longitude) -> None:
        print("Moved to ", latitude, longitude)
        self.ui.Overview_map_view.setHtml(load_map([latitude, longitude]))

    def onMapRClick(self, latitude, longitude) -> None:
        print("RClick on ", latitude, longitude)

    def onMapLClick(self, latitude, longitude) -> None:
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude) -> None:
        print("DClick on ", latitude, longitude)

    def onMapGeojson(self, json) -> None:
        # Handle the received GeoJSON data
        coordinates = geojson_to_coordinates(json)
        print(coordinates)
