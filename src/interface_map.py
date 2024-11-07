# PyQt5
import datetime
import sys

from asyncqt import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

# user-defined modules
from config import *
from interface_base import *
from UI.interface_uav import *
from utils.drone_utils import *
from utils.map_folium import *
from utils.map_utils import *
from utils.qt_utils import *


class Map(Interface):
    def __init__(self):
        Interface.__init__(self)
        self._init_map()
        self._init_map_events()

    def _init_map(self):
        # map URL
        # file:///.../SwarmUAV-UET/assets/map.html
        self.ui.MapWebView.setUrl(QtCore.QUrl(map_html_path))
        # self.rescue_map_data = MapFolium(
        #     [21.064862, 105.792958], 16, plugins=["Draw", "Geocoder", "MeasureControl", "MiniMap"]
        # )
        # self.ui.MapWebView.setHtml(self.rescue_map_data.render_map())
        # map engine
        self.rescue_map = MapEngine(self.ui.MapWebView)
        self.rescue_map.mapMovedCallback = self.onMapMoved
        self.rescue_map.mapClickedCallback = self.onMapLClick
        self.rescue_map.mapDoubleClickedCallback = self.onMapDClick
        self.rescue_map.mapRightClickedCallback = self.onMapRClick
        self.rescue_map.mapGeojsonCallback = self.onMapGeojson

        # Ovv map only for seeing
        self.ovv_map_data = MapFolium(
            [21.064862, 105.792958], 16, plugins=["Geocoder", "MeasureControl", "MiniMap"]
        )
        # self.ui.Overview_map_view.setUrl(QtCore.QUrl(map_html_path))
        self.ui.Overview_map_view.setHtml(self.ovv_map_data.render_map())
        self.ovv_map = MapEngine(self.ui.Overview_map_view)
        #
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

    def _init_map_events(self):
        self.ui.btn_map_show_drones.clicked.connect(self.btn_show_drones_callback)
        self.ui.btn_map_show_points.clicked.connect(self.btn_show_points_callback)
        self.ui.btn_map_refresh_data.clicked.connect(self.btn_refresh_data_callback)
        self.ui.btn_map_export_points.clicked.connect(self.btn_export_points_callback)

        self.ui.btn_map_split_area.clicked.connect(self.btn_split_area_callback)
        self.ui.btn_map_export_grid.clicked.connect(self.btn_export_grid_callback)
        self.ui.btn_map_toggle_route.clicked.connect(self.btn_toggle_route_callback)

    # -----------------------------< map event functions >--------------------------------
    def btn_show_drones_callback(self):
        # get gps from drones gps.log file and show on map
        # NOTE: draw to ui
        pass

    def btn_show_points_callback(self):
        # read points from file and show on map
        pass

    def btn_refresh_data_callback(self):
        # read points from map interface and update to database
        pass

    def btn_export_points_callback(self):
        # export points to file
        pass

    def btn_split_area_callback(self):
        # split area to grid
        pass

    def btn_export_grid_callback(self):
        # export grid to file
        pass

    def btn_toggle_route_callback(self):
        # toggle route line and points
        pass

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
        html = self.ovv_map_data.center_to(latitude, longitude)
        self.ui.Overview_map_view.setHtml(html)

    def onMapRClick(self, latitude, longitude) -> None:
        print("RClick on ", latitude, longitude)

    def onMapLClick(self, latitude, longitude) -> None:
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude) -> None:
        print("DClick on ", latitude, longitude)

    def onMapGeojson(self, json) -> None:
        # Handle the received GeoJSON data
        try:
            coordinates = geojson_to_coordinates(json)
            type, points = coordinates

            if type == "Point":
                lon, lat = points
                html = self.ovv_map_data.add_marker(
                    type, float(lat), float(lon), icon={"color": "blue", "icon": "map-pin"}
                )
            elif type == "Polygon":
                points = [[float(lat), float(lon)] for lon, lat in points[0]]
                html = self.ovv_map_data.add_polygon(type, points)

            elif type == "LineString":
                points = [[float(lat), float(lon)] for lon, lat in points]
                html = self.ovv_map_data.add_line(type, points)

            self.ui.Overview_map_view.setHtml(html)
        except Exception as e:
            print(repr(e))


# ------------------------------------< Map Application Class >-----------------------------
def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Oxygen")  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = Map()
    MainWindow.show()

    with loop:
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        sys.exit(loop.run_forever())


if __name__ == "__main__":
    run()
