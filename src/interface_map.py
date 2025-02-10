# !/usr/bin/env python3
import copy
import datetime
import pprint
import sys
from pathlib import Path

# PyQt5
import pytz
from asyncqt import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

# user-defined modules
from config.interface_config import *
from config.stream_config import *
from config.uav_config import *
from interface_base import *
from Qt.interface_uav import *
from utils.calculation_helpers import *

#
from utils.drone_utils import *
from utils.map_engine import *
from utils.map_folium import *
from utils.map_helpers import *
from utils.qt_utils import *

vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
__current_time__ = datetime.datetime.now(vietnam_tz)
parent_dir = Path(__file__).parent.parent

# cspell: ignore Minh qtwebchannel geocoder asyncio, asyncqt, geojson, geojsons, html, htm, lon, lat, lst, uav, uavs, uav_index, uav_indexs

# Define the path to the assets/icons directory
drone_icon_path = "../assets/icons/drone.png"
dot_icon_path = "../assets/icons/red_dot.png"

rotated_area_list = []
grid_enabled = False
grid_points = []
final_grid = []

"""NOTE:
Main map: leaflet.js (html)
- Draw points, lines, polygons
- Get data of points, lines, polygons as GeoJSON (save to files, and send via qtwebchannel)
- Add draw makers, lines, polygons from GeoJSON data or st else.
Ovv map: folium (python): one-way from python to html
- Draw points, lines, polygons from GeoJSON data
"""


class Map(Interface):
    """Map class for the interface

    Args:
        Interface (QApplication): ...
    """

    debug = True

    noArea = 5
    gridSize = 10  # meters

    position_list = []
    geodata = {}

    number = 0

    drone_num = 5
    drone_position_list = []
    drone_marker_list = []
    drone_station_position = None

    def __init__(self):
        Interface.__init__(self)
        self._init_map()
        self._init_map_events()

    def _init_map(self):
        # set tab to map
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)

        # Rescue map
        self.rescue_map = MapEngine(
            name="Rescue Map", widget=self.ui.MapWebView, url=map_html_path
        )
        self.rescue_map.mapMovedCallback = self.onMapMoved
        self.rescue_map.mapClickedCallback = self.onMapLClick
        self.rescue_map.mapDoubleClickedCallback = self.onMapDClick
        self.rescue_map.mapRightClickedCallback = self.onMapRClick

        self.rescue_map.markerMovedCallback = self.onMarkerMoved
        self.rescue_map.markerClickedCallback = self.onMarkerLClick
        self.rescue_map.markerDoubleClickedCallback = self.onMarkerDClick
        self.rescue_map.markerRightClickedCallback = self.onMarkerRClick

        self.rescue_map.mapGeojsonCallback = self.onMapGeojson

        self.rescue_map.setZoom(30)
        self.rescue_map.waitUntilReady()

        # Ovv map (only for watching)
        # self.ovv_map_data = MapFolium(
        #     [21.064862, 105.792958], 16, plugins=["Geocoder", "MeasureControl", "MiniMap"]
        # )

        # self.ui.Overview_map_view.setHtml(self.ovv_map_data.render_map())
        self.ovv_map = MapEngine(
            name="Overview Map",
            widget=self.ui.Overview_map_view,
            url=map_ovv_html_path,
        )
        self.ovv_map.mapMovedCallback = self.onMapOvvMoved
        self.ovv_map.mapClickedCallback = self.onMapLClick
        self.ovv_map.mapDoubleClickedCallback = self.onMapDClick
        self.ovv_map.mapRightClickedCallback = self.onMapRClick

        self.ovv_map.waitUntilReady()

        #
        self.ui.dateTimeEdit.setDateTime(__current_time__)

        # Initialize the timer and set update flag
        # ...

        # Show drones on the map
        self.show_drones()

    def _init_map_events(self):
        # Connect the buttons to the callback functions
        self.ui.btn_map_create_routes.clicked.connect(self.btn_map_create_routes_callback)
        self.ui.btn_map_show_grid_points.clicked.connect(self.btn_map_show_grid_points_callback)
        self.ui.btn_map_refresh_data.clicked.connect(self.btn_refresh_data_callback)
        self.ui.btn_map_export_plan.clicked.connect(self.btn_map_export_plan_callback)
        self.ui.btn_map_split_area.clicked.connect(self.btn_split_area_callback)
        self.ui.btn_map_reduce_points.clicked.connect(self.btn_map_reduce_points_callback)
        self.ui.btn_map_toggle_route.clicked.connect(self.btn_toggle_route_callback)
        #
        # self.ui.noArea_value.installEventFilter(self)
        self.ui.noArea_line_edit.returnPressed.connect(self.noArea_line_edit_callback)
        self.ui.gridSize_line_edit.returnPressed.connect(self.gridSize_line_edit_callback)

    # -----------------------------< map event functions >--------------------------------

    def btn_map_create_routes_callback(self):
        """Create routes for drones"""
        if self.debug:
            print("Button clicked: Create routes")

        try:
            print("Creating routes")
            # develop later
        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_map_show_grid_points_callback(self):
        """Open local file (txt) and show points on the map
        File template:
        lat1, lon1
        lat2, lon2
        ...
        """
        if self.debug:
            print("Button clicked: Show grid points")

        try:
            grid_size = self.gridSize
            n_areas = min(self.noArea, self.drone_num)
            if grid_size <= 0 or n_areas <= 0:
                logger.log("Invalid grid size or number of areas", level="error")
                return
            grid_points = split_grids(self.rotated_area_list, *self.extra, grid_size, n_areas)
            self.multi_area = True if n_areas > 1 else False
            if self.debug:
                print(f"Multi Area: {self.multi_area} | Grid points:")
                pprint.pprint(grid_points)

            # Show grid points on the map
            # TODO(fix me): not showed enough points
            self.process_grid_points(grid_points)
            self.grid_enabled = True

        except Exception as e:
            logger.log(repr(e), level="error")

    def process_grid_points(self, grid_points):
        self.area_marker = []
        if self.multi_area:
            for ind, area in enumerate(grid_points):
                self.ordered_grid_points = find_path(area, self.drone_position_list[0])
                # self.ordered_grid_points lặp đi lặp lại thì nó chả plot có vai điểm r ẩn các điểm trc đó?? viết code ngu vc
                for i, point in enumerate(self.ordered_grid_points):
                    self.rescue_map.addMarker(
                        f"A{ind + 1}P{i + 1}",
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                    self.ovv_map.addMarker(
                        f"A{ind + 1}P{i + 1}",
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                    self.area_marker.append(f"A{ind + 1}P{i + 1}")
                # write to file
                with open(f"{parent_dir}/src/logs/points/points{ind + 1}.txt", "w") as file:
                    for lat, lon in self.ordered_grid_points:
                        file.write(f"{lat}, {lon}\n")
        else:
            self.ordered_grid_points = find_path(grid_points, self.drone_position_list[0])
            for i, point in enumerate(self.ordered_grid_points):
                self.rescue_map.addMarker(
                    f"A{1}P{i + 1}",
                    float(point[0]),
                    float(point[1]),
                    **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                )
                self.ovv_map.addMarker(
                    f"A{1}P{i + 1}",
                    float(point[0]),
                    float(point[1]),
                    **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                )
                self.area_marker.append(f"A{1}P{i + 1}")

            # write to file
            with open(f"{parent_dir}/src/logs/points/points1.txt", "w") as file:
                for lat, lon in self.ordered_grid_points:
                    file.write(f"{lat}, {lon}\n")

    def btn_refresh_data_callback(self):
        # TODO: Refresh the data on the map
        if self.debug:
            print("Button clicked: Refresh data")
        try:
            # read points from files
            points_from_file = []

            filename = QFileDialog.getOpenFileName(
                parent=self,
                caption="Open map file",
                directory=f"{parent_dir}/src/logs/area/",
                initialFilter="Files (*.TXT *.txt *.plan)",
            )[0]
            # print("Open file:", filename)
            if filename:
                with open(file=filename, mode="r") as file:
                    data = file.read().strip().split("\n")
                    for line in data:
                        lat, lon = line.split(",")
                        points_from_file.append([float(lat), float(lon)])
            else:
                logger.log("No file selected, plotting default grid", level="warning")
                points_from_file = self.geodata.get("Points", [])

            if len(points_from_file) < 3:
                print("Invalid area points, must be at least 3 points")
                return

            # from position list to polygon, line, and markers draws as geojson
            geojson = {}

            if points_from_file[0] != points_from_file[-1]:
                points_from_file.append(points_from_file[0])

            geojson.setdefault("Polygon", []).extend(points_from_file[:])

            for ind, (lat, lon) in enumerate(points_from_file[:-1]):
                geojson.setdefault("Points", []).append([float(lat), float(lon)])
                geojson.setdefault("LineString", []).append(
                    [points_from_file[ind], points_from_file[ind + 1]]
                )

            if self.debug:
                print("GeoJSON data:", geojson)

            # compare to current point and update
            # ...

            # show geodata on the map
            self.show_geodata(geojson)
            pass
        except Exception as e:
            logger.log(repr(e), level="error")
        pass

    def btn_map_export_plan_callback(self):
        """Get points from the map and export to a .txt file"""
        # TODO: Export the plan to a .plan file
        if self.debug:
            print("Button clicked: Export plan")

        try:
            # Define the path to save the .plan file
            pass
            # export points to file
            # Define the structure of the .plan file according to QGroundControl specifications

        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_split_area_callback(self):
        """Split area into grid and show on the map
        1. Get the polygon points
        2. Get the number of `n_areas`
        3. Split the polygon into `n_areas` parts
        """
        self.splitted_areas = []

        if self.debug:
            print("Button clicked: Split area")

        try:
            # Confirm the polygon is closed
            if self.geodata.get("Polygon") is None:
                logger.log("No polygon data to split", level="error")
                return

            # Get the polygon points
            polygon_points = self.geodata["Polygon"][0]
            if len(polygon_points) < 3:
                logger.log("Invalid polygon points, at least 3 points needed", level="error")
                print("Got:", polygon_points)
                return

            n_areas = min(self.noArea, self.drone_num)  # number of areas to split
            logger.log(f"Splitting the area into {n_areas} areas", level="info")

            # split the polygon into n_areas parts
            # Stupid code from Thang lol nao do, dhs tach 1 dong param ra 2 ham???
            splitted_areas, rotated_area_list, angle, midpoint, min_lat, min_lon = (
                split_polygon_into_areas_old(polygon_points, n_areas)
            )

            for ind, area in enumerate(splitted_areas):
                if self.debug:
                    print(f"Area {ind}: {area}")

                if area[0] != area[-1]:
                    area.append(area[0])

                self.rescue_map.drawPolygon(
                    f"Area_{ind}",
                    area,
                    options=dict(
                        color="blue", weight=2, fill=True, fillColor="blue", fillOpacity=0.2
                    ),
                )
                self.ovv_map.drawPolygon(
                    f"Area_{ind}",
                    area,
                    options=dict(
                        color="blue", weight=2, fill=True, fillColor="blue", fillOpacity=0.2
                    ),
                )

                # Save the rotated area list
                with open(f"{parent_dir}/src/logs/area/area{ind + 1}.txt", "w") as file:
                    for lat, lon in area:
                        file.write(f"{lat}, {lon}\n")

            self.grid_points_list = copy.deepcopy(rotated_area_list)
            self.rotated_area_list = rotated_area_list
            self.extra = (angle, midpoint, min_lat, min_lon)

        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_map_reduce_points_callback(self):
        """Reduce the number of grid points by
        removing the middle points of each line, keeping the end points
        """
        # TODO: Reduce the number of grid points
        if self.debug:
            print("Button clicked: Reduce points")

        try:
            pass
        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_toggle_route_callback(self):
        # TODO: Toggle the route on the map (through the grid points)
        # Toggle the route on the map (through the grid points)
        if self.debug:
            print("Button clicked: Toggle route")

        try:
            print("Toggling route")
        except Exception as e:
            logger.log(repr(e), level="error")

    def noArea_line_edit_callback(self):
        try:
            self.noArea = int(self.ui.noArea_line_edit.text().strip())
            print("Set noArea to:", self.noArea)
        except Exception as e:
            logger.log(repr(e), level="error")

    def gridSize_line_edit_callback(self):
        try:
            self.gridSize = int(self.ui.gridSize_line_edit.text().strip())
            print("Set gridSize to:", self.gridSize)
        except Exception as e:
            logger.log(repr(e), level="error")

    # -----------------------------< custom map functions >-----------------------------
    # Marker events: moved, clicked, double clicked, right clicked
    def onMarkerMoved(self, key, latitude, longitude) -> None:
        if self.debug:
            print("Marker moved!!", key, latitude, longitude)
        pass

    def onMarkerRClick(self, key, latitude, longitude) -> None:
        if self.debug:
            print("Marker RClick on ", key, latitude, longitude)
        pass

    def onMarkerLClick(self, key, latitude, longitude) -> None:
        if self.debug:
            print("Marker LClick on ", key, latitude, longitude)
        pass

    def onMarkerDClick(self, key, latitude, longitude) -> None:
        if self.debug:
            print("Marker DClick on ", key, latitude, longitude)
        pass

    # Map events: moved, clicked, double clicked, right clicked
    def onMapMoved(self, latitude, longitude) -> None:
        if self.debug:
            print("Main map moved to ", latitude, longitude, "Move Ovv map to the same position")
        try:
            self.ovv_map.centerAt(latitude, longitude)
        except Exception as e:
            logger.log(repr(e), level="error")

    def onMapOvvMoved(self, latitude, longitude) -> None:
        if self.debug:
            print("Ovv map moved to ", latitude, longitude, "Move Main map to the same position")
        try:
            self.rescue_map.centerAt(latitude, longitude)
        except Exception as e:
            logger.log(repr(e), level="error")

    def onMapRClick(self, latitude, longitude) -> None:
        if self.debug:
            print("RClick on ", latitude, longitude)
        pass

    def onMapLClick(self, latitude, longitude) -> None:
        if self.debug:
            print("LClick on ", latitude, longitude)
        pass

    def onMapDClick(self, latitude, longitude) -> None:
        if self.debug:
            print("DClick on ", latitude, longitude)
        pass

    # GeoJSON data received from the map
    def onMapGeojson(self, json) -> None:
        """
        Handles the GeoJSON data and updates the map accordingly.
        Parameters:
        json (dict): The GeoJSON data to be processed.
        The function processes the GeoJSON data to extract coordinates and type of geometry.
        Depending on the type of geometry (Point, Polygon, LineString), it performs the following actions:
        - For Point: Adds a marker to the map and appends the position to the position list.
        - For Polygon: Calculates the area, updates the area label, displays the polygon on the map, and exports the coordinates to a file.
        - For LineString: Draws a polyLine on the map.
        The function also logs any exceptions that occur during processing.
        """

        try:
            coordinates = geojson_to_coordinates(json)
            type, points = coordinates

            if type == "Point":
                lon, lat = points
                self.ovv_map.addMarker("Point", lat, lon, icon=dot_icon_path)
                self.position_list.append((lat, lon))

            elif type == "Polygon":
                points = [[float(lat), float(lon)] for lon, lat in points[0]]

                # calculate the area of the polygon
                area = area_of_polygon(points)
                # display to the area label
                self.ui.area_value.setText(str(round(area["ha"], 2)) + " ha")

                # display the polygon on the ovv map
                self.ovv_map.drawPolygon(type, points)

                # export to current area file
                with open(f"{parent_dir}/src/logs/area/current_area.txt", "w") as file:
                    for lat, lon in points:
                        file.write(f"{lat}, {lon}\n")

            elif type == "LineString":
                points = [[float(lat), float(lon)] for lon, lat in points]
                self.ovv_map.drawPolyLine(type, points)

            self.geodata.setdefault(type, []).append(points)

        except Exception as e:
            logger.log(repr(e), level="error")

    def show_drones(self) -> None:
        for i in range(self.drone_num):
            with open(f"{parent_dir}/src/logs/drone_init_pos/uav_{i + 1}.txt", "r") as file:
                lat, lon = map(float, file.readline().strip().split(","))
                self.drone_position_list.append((lat, lon))
                self.rescue_map.addMarker(
                    key=f"uav_{i}",
                    latitude=lat,
                    longitude=lon,
                    **dict(
                        icon=drone_icon_path,
                        draggable=True,
                        title=f"UAV {i}",
                        iconSize={"width": 21, "height": 21},
                    ),
                )
                self.ovv_map.addMarker(
                    key=f"uav_{i}",
                    latitude=lat,
                    longitude=lon,
                    **dict(
                        icon=drone_icon_path,
                        draggable=True,
                        title=f"UAV {i}",
                        iconSize={"width": 21, "height": 21},
                    ),
                )
                self.drone_marker_list.append(i + 1)
        # assign the first drone as the station
        self.drone_station_position = self.drone_position_list[0]

    def show_geodata(self, geodata: dict) -> None:
        # Show the points on the rescue map
        for ind, (lat, lon) in enumerate(geodata["Points"]):
            self.rescue_map.addMarker(
                str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(dot_icon_path), iconSize={"width": 10, "height": 10}),
            )
            self.ovv_map.addMarker(
                str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(dot_icon_path), iconSize={"width": 10, "height": 10}),
            )
            if self.debug:
                print(f"Added marker {ind} at {lat}, {lon}")

        # Show the line on the rescue map
        for ind, (start, end) in enumerate(geodata["LineString"]):
            self.rescue_map.drawPolyLine(
                str(ind), [start, end], options=dict(color="yellow", weight=5)
            )
            self.ovv_map.drawPolyLine(
                str(ind), [start, end], options=dict(color="yellow", weight=5)
            )
            if self.debug:
                print(f"Added line {ind} from {start} to {end}")

        # Show the polygon on the rescue map
        self.rescue_map.drawPolygon(
            "Polygon",
            geodata["Polygon"],
            options=dict(color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2),
        )
        self.ovv_map.drawPolygon(
            "Polygon",
            geodata["Polygon"],
            options=dict(color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2),
        )
        pass


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
    run()
