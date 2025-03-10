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

"""NOTE:
Main map: leaflet.js (html)
- Draw points, lines, polygons
- Get data of points, lines, polygons as GeoJSON (save to files, and send via qtwebchannel)
- Add draw makers, lines, polygons from GeoJSON data or st else.
Ovv map: leaflet.js (html): one-way from python to html
- Draw points, lines, polygons from GeoJSON data
"""


class Map(Interface):
    """Map class for the interface

    Args:
        Interface (QApplication): ...
    """

    debug = False

    noArea = 5
    drone_num = 5
    gridSize = 10  # meters

    drone_path_enabled = False
    reduced_grid_points = False
    refreshed = False
    geodata = {}

    drone_areas_dict = {}
    drone_paths_dict = {}
    drone_markers_dict = {}
    drone_initial_positions = {}

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

        # NOTE: Ovv map (only for watching)
        # (This part is based on folium, so it's one-way from python to html)
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

        # set initial values
        self.ui.noArea_line_edit.setText(str(self.noArea))
        self.ui.gridSize_line_edit.setText(str(self.gridSize))
        self.ui.dateTimeEdit.setDateTime(__current_time__)

        # TODO(future): Initialize the timer and set update flag, to read the drone position every ... seconds
        # ...

        # Show drones on the map
        self.show_drones()

    def _init_map_events(self):
        """
        Initializes the map events by connecting UI buttons and line edit widgets to their respective callback functions
        """

        # Connect the buttons to the callback functions
        self.ui.btn_map_create_routes.clicked.connect(self.btn_map_create_routes_callback)
        self.ui.btn_map_show_grid_points.clicked.connect(self.btn_map_show_grid_points_callback)
        self.ui.btn_map_refresh_data.clicked.connect(self.btn_refresh_data_callback)
        self.ui.btn_map_export_plan.clicked.connect(self.btn_map_export_plan_callback)
        self.ui.btn_map_split_area.clicked.connect(self.btn_split_area_callback)
        self.ui.btn_map_reduce_points.clicked.connect(self.btn_map_reduce_points_callback)
        self.ui.btn_map_toggle_route.clicked.connect(self.btn_toggle_route_callback)
        #

        # connect line edit to callback functions
        self.ui.noArea_line_edit.returnPressed.connect(self.noArea_line_edit_callback)
        self.ui.gridSize_line_edit.returnPressed.connect(self.gridSize_line_edit_callback)

    # -----------------------------< map event functions >--------------------------------

    def btn_map_create_routes_callback(self):
        """Create routes for drones"""

        if self.debug:
            print("Button clicked: Create routes")

        try:
            colors = ["red", "blue", "green", "yellow", "purple", "orange"]
            color_index = 0
            # key = "A{ind + 1}P{j - 1}-{j}" : key for the path Area ind from Point j-1 to j
            if self.drone_path_enabled:
                # Remove all previous markers
                self.remove_objects(["paths"])
                self.drone_paths_dict = {}
                self.drone_path_enabled = False
                return
            else:
                self.drone_path_enabled = True
                self.drone_paths_dict = {}

                area_grid_points = {}
                for key, value in self.drone_markers_dict.items():
                    area_index = int(key.split("A")[1].split("P")[0])
                    point_index = int(key.split("P")[1])
                    area_grid_points.setdefault(area_index, []).append(value)

                for ind, (_, value) in enumerate(area_grid_points.items()):
                    color = colors[color_index]
                    color_index = (color_index + 1) % len(colors)

                    # first path is from uav to the first nearest point
                    start = self.drone_position_list[ind]
                    end = value[0]

                    self.rescue_map.drawPolyLine(
                        f"A{ind + 1}P{0}-{1}", [start, end], options=dict(color=color, weight=5)
                    )
                    self.ovv_map.drawPolyLine(
                        f"A{ind + 1}P{0}-{1}", [start, end], options=dict(color=color, weight=5)
                    )
                    self.drone_paths_dict[f"A{ind + 1}P{0}-{1}"] = (start, end)

                    # within area
                    for j in range(len(value)):
                        if j == 0:
                            continue
                        start = value[j - 1]
                        end = value[j]

                        self.rescue_map.drawPolyLine(
                            f"A{ind + 1}P{j}-{j + 1}",
                            [start, end],
                            options=dict(color=color, weight=5),
                        )
                        self.ovv_map.drawPolyLine(
                            f"A{ind + 1}P{j}-{j + 1}",
                            [start, end],
                            options=dict(color=color, weight=5),
                        )
                        self.drone_paths_dict[f"A{ind + 1}P{j}-{j + 1}"] = (start, end)

                return
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

            if self.debug:
                print(f"Multi Area: {self.multi_area} | Grid points:")
                pprint.pprint(grid_points)

            # if exist, show the grid points on the map
            if (self.reduced_grid_points or self.refreshed) and (self.drone_markers_dict != {}):
                self.remove_objects(["markers"])

                for key, value in self.drone_markers_dict.items():
                    self.rescue_map.addMarker(
                        key,
                        float(value[0]),
                        float(value[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                    self.ovv_map.addMarker(
                        key,
                        float(value[0]),
                        float(value[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                return

            # Split the area into grid points
            grid_points = split_grids(self.rotated_area_list, *self.extra, grid_size, n_areas)

            self.multi_area = True if n_areas > 1 else False
            # Remove all previous markers
            self.remove_objects(["markers"])
            self.drone_markers_dict = {}

            # Show grid points on the map
            self.process_grid_points(grid_points)
            self.grid_enabled = True

        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Error: {repr(e)}, try to modify the grid size or number of areas",
                src_msg="Show grid points",
                type_msg="error",
            )

    def process_grid_points(self, grid_points):
        try:
            # Show grid points on the map
            self.reduced_grid_points = False
            self.refreshed = False

            if self.multi_area:
                for ind, area in enumerate(grid_points):
                    self.ordered_grid_points = find_path(area, self.drone_position_list[0])
                    self.ordered_grid_points = remove_duplicate_pts(self.ordered_grid_points)

                    # avoid plotting too many points
                    if len(self.ordered_grid_points) > 100:
                        logger.log(
                            "Two many points to plot, try to increase grid size!!", level="warning"
                        )
                        return

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

                        self.drone_markers_dict[f"A{ind + 1}P{i + 1}"] = point

                    # write to file
                    with open(f"{parent_dir}/src/logs/points/points{ind + 1}.txt", "w") as file:
                        for lat, lon in self.ordered_grid_points:
                            file.write(f"{lat}, {lon}\n")
            else:
                self.ordered_grid_points = find_path(grid_points, self.drone_position_list[0])
                self.ordered_grid_points = remove_duplicate_pts(self.ordered_grid_points)

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

                    self.drone_markers_dict[f"A{1}P{i + 1}"] = point

                # write to file
                with open(f"{parent_dir}/src/logs/points/points1.txt", "w") as file:
                    for lat, lon in self.ordered_grid_points:
                        file.write(f"{lat}, {lon}\n")

        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Error: {repr(e)}, try to modify the grid size or number of areas",
                src_msg="Show grid points",
                type_msg="error",
            )

    def btn_refresh_data_callback(self):
        """Refresh the data on the map"""

        if self.debug:
            print("Button clicked: Refresh data")

        try:
            # read points from files
            points_from_file = []

            filename = QFileDialog.getOpenFileName(
                parent=self,
                caption="Open map file",
                directory=f"{parent_dir}/src/logs/",
                initialFilter="Files (*.json)",
            )[0]
            # print("Open file:", filename)
            if filename:
                with open(filename, "r") as file:
                    data = json.load(file)
            else:
                logger.log("No file selected, plotting default grid", level="warning")
                return
            """
            data = {
                "Area": self.geodata.get("Polygon", []),
                "Points": self.geodata.get("Points", []),
                "LineString": self.geodata.get("LineString", []),
                "Drone areas:": {
                    key: value for key, value in self.drone_areas_dict.items()
                },
                "Drone grid points": {
                    key: value for key, value in self.drone_markers_dict.items()
                },
                "Drone paths": {key: value for key, value in self.drone_paths_dict.items()},
            }
            """
            self.geodata["Polygon"] = data.get("Area", [])
            self.geodata["Points"] = data.get("Points", [])
            self.geodata["LineString"] = data.get("LineString", [])
            self.drone_areas_dict = data.get("Drone areas:", {})
            self.drone_markers_dict = data.get("Drone grid points", {})
            # TODO: update path following the grid points
            self.drone_paths_dict = data.get("Drone paths", {})

            logger.log("Updated data on the map", level="info")

            # NOTE: All point of polygon is fixed, if you want to change it, please delete the data file
            self.popup_msg(
                "Data updated successfully, please re-process",
                src_msg="Refresh data",
                type_msg="info",
            )
            self.refreshed = True

            return

        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_map_export_plan_callback(self, to_plan_format=False):
        """Get points from the map and export to a .txt file"""

        if self.debug:
            print("Button clicked: Export plan")

        try:
            # # Define the structure of the .plan file according to QGroundControl specifications
            # # Define the structure of the .plan file according to QGroundControl specifications
            # if to_plan_format:
            #     plan_data = {
            #         "fileType": "Plan",
            #         "geoFence": {"circles": [], "polygons": [], "version": 2},
            #         "groundStation": "QGroundControl",
            #         "mission": {
            #             "cruiseSpeed": 5,  # Set cruise speed in m/s
            #             "hoverSpeed": 1,  # Set hover speed in m/s
            #             "firmwareType": 12,  # Specify the firmware type (e.g., PX4)
            #             "globalPlanAltitudeMode": 1,  # Altitude mode
            #             "items": [],
            #             "plannedHomePosition": [0, 0, 0],  # Placeholder for home position
            #             "vehicleType": 2,  # Type of vehicle (e.g., 2 for fixed-wing)
            #             "version": 2,
            #         },
            #         "rallyPoints": {"points": [], "version": 2},  # Initialize with empty points
            #         "version": 1,
            #     }
            #     for i, (key, value) in enumerate(self.area_grid_points.items()):
            #         # Todo: Add the grid points to the plan_data
            #         pass

            # Todo: export polygon, grid points, lines to .json file
            file_path = f"{parent_dir}/src/logs/map_data/map_runtime_{__current_time__.strftime('%Y-%m-%d_%H-%M-%S')}.json"

            data = {
                "Area": self.geodata.get("Polygon", []),
                "Points": self.geodata.get("Points", []),
                "LineString": self.geodata.get("LineString", []),
                "Drone areas:": {key: area for key, area in self.drone_areas_dict.items()},
                "Drone grid points": {
                    key: value for key, value in self.drone_markers_dict.items()
                },
                "Drone paths": {key: value for key, value in self.drone_paths_dict.items()},
            }

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            logger.log(f"Exported data to {file_path}", level="info")
            self.popup_msg(
                f"Exported data to {file_path}",
                src_msg="Export plan",
                type_msg="info",
            )
            return

        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_split_area_callback(self):
        """Split area into grid and show on the map
        1. Get the polygon points
        2. Get the number of `n_areas`
        3. Split the polygon into `n_areas` parts
        """

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

            if self.debug:
                print("Receive polygon points:", polygon_points)

            # Remove all previous markers
            self.remove_objects(["markers", "paths", "areas"])
            self.drone_areas_dict = {}

            # get the number of areas to split
            n_areas = min(self.noArea, self.drone_num)  # number of areas to split
            logger.log(f"Splitting the area into {n_areas} areas", level="info")

            # split the polygon into n_areas parts
            splitted_areas, rotated_area_list, angle, midpoint, min_lat, min_lon = (
                split_polygon_into_areas_old(polygon_points, n_areas)
            )

            # draw the splitted areas on the map
            for ind, area in enumerate(splitted_areas):
                if self.debug:
                    print(f"Area {ind}: {area}")

                if area[0] != area[-1]:
                    area.append(area[0])

                key = f"Area_{ind}"
                self.rescue_map.drawPolygon(
                    key=key,
                    coordinates=area,
                    options=dict(
                        color="blue", weight=2, fill=True, fillColor="blue", fillOpacity=0.2
                    ),
                )
                self.ovv_map.drawPolygon(
                    key=key,
                    coordinates=area,
                    options=dict(
                        color="blue", weight=2, fill=True, fillColor="blue", fillOpacity=0.2
                    ),
                )
                self.drone_areas_dict[key] = area

                # Save the rotated area list
                with open(f"{parent_dir}/src/logs/area/area{ind + 1}.txt", "w") as file:
                    for lat, lon in area:
                        file.write(f"{lat}, {lon}\n")

            # copy to the class variables
            self.rotated_area_list = rotated_area_list
            self.extra = (angle, midpoint, min_lat, min_lon)

        except Exception as e:
            logger.log(repr(e), level="error")

    def btn_map_reduce_points_callback(self):
        """Reduce the number of grid points by
        removing the middle points of each line, keeping the end points
        """
        # NOTE: This function only reduces number of points in the grid, not number of paths in routes
        reduced_grid_point_list = []
        if self.debug:
            print("Button clicked: Reduce points")

        try:
            # get data from previous grid points
            area_grid_points = {}
            for key, value in self.drone_markers_dict.items():
                area_index = int(key.split("A")[1].split("P")[0])
                point_index = int(key.split("P")[1])
                area_grid_points.setdefault(area_index, []).append(value)

            # delete point from map
            self.remove_objects(["markers"])
            self.drone_markers_dict = {}

            # reduce the number of points
            for ind, points_in_area in enumerate(area_grid_points.values()):
                if len(points_in_area) < 3:
                    reduced_grid_point_list.append(points_in_area)
                    continue

                filtered_points = [points_in_area[0]]
                i = 1
                while i < len(points_in_area) - 1:
                    if point_on_line(
                        points_in_area[i - 1], points_in_area[i], points_in_area[i + 1]
                    ):
                        i += 1
                    else:
                        filtered_points.append(points_in_area[i])
                        i += 1
                filtered_points.append(points_in_area[-1])

                for i, point in enumerate(filtered_points):
                    self.rescue_map.addMarker(
                        f"A{ind + 1}P{i + 1}",
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                    self.ovv_map.addMarker(
                        f"A{ind+ 1}P{i + 1}",
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(dot_icon_path), iconSize={"width": 5, "height": 5}),
                    )
                    self.drone_markers_dict[f"A{ind+ 1}P{i + 1}"] = point

                reduced_grid_point_list.append(filtered_points)
                self.reduced_grid_points = True

            for i, points in enumerate(reduced_grid_point_list):
                with open(f"{parent_dir}/src/logs/points/reduced_point{i + 1}.txt", "w") as file:
                    for lat, lon in points:
                        file.write(f"{lat}, {lon}\n")

        except Exception as e:
            logger.log(repr(e), level="error")
            pass

    def btn_toggle_route_callback(self):
        # Toggle the route on the map (through the grid points)
        if self.debug:
            print("Button clicked: Toggle route")

        try:
            # print("Toggling route")
            self.btn_map_show_grid_points_callback()
            self.btn_map_create_routes_callback()
            # self.drone_path_enabled = not self.drone_path_enabled
        except Exception as e:
            logger.log(repr(e), level="error")

    def noArea_line_edit_callback(self):
        try:
            self.noArea = int(self.ui.noArea_line_edit.text().strip())
            print("Set noArea to:", self.noArea)
            self.refreshed = False
            self.reduced_grid_points = False
        except Exception as e:
            logger.log(repr(e), level="error")

    def gridSize_line_edit_callback(self):
        try:
            self.gridSize = int(self.ui.gridSize_line_edit.text().strip())
            print("Set gridSize to:", self.gridSize)
            self.refreshed = False
            self.reduced_grid_points = False
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

            self.geodata.setdefault(type, []).clear()  # clear the previous data
            self.remove_objects(["markers", "paths", "areas"])
            
            if type == "Point":
                lon, lat = points
                self.ovv_map.deleteMarker(type)
                self.ovv_map.addMarker("Point", lat, lon, icon=dot_icon_path)

            elif type == "LineString":
                points = [[float(lat), float(lon)] for lon, lat in points]
                self.ovv_map.deletePolyLine(type)
                self.ovv_map.drawPolyLine(type, points)

            elif type == "Polygon":
                points = [[float(lat), float(lon)] for lon, lat in points[0]]

                # calculate the area of the polygon
                area = area_of_polygon(points)
                # display to the area label
                self.ui.area_value.setText(str(round(area["ha"], 2)) + " ha")

                # display the polygon on the ovv map
                self.ovv_map.deletePolygon(type)
                self.ovv_map.drawPolygon(type, points)
                # TODO (fixme): maybe the overall polygon is diff
                # # export to current area file
                # with open(f"{parent_dir}/src/logs/area/current_area.txt", "w") as file:
                #     for lat, lon in points:
                #         file.write(f"{lat}, {lon}\n")

            self.geodata.setdefault(type, []).append(points)
            
            # reset variables
            self.refreshed = False
            self.reduced_grid_points = False           

        except Exception as e:
            logger.log(repr(e), level="error")
            
    def remove_objects(self, objs:str=[]) -> None:
        # TODO: ovv map not del the polygon, only point
        if self.debug:
            print("Removing objects:", objs)
        try:
            if objs == []:
                return
            for obj in objs:
                if obj == 'markers':
                    for key in self.drone_markers_dict.keys():
                        self.rescue_map.deleteMarker(key)
                        self.ovv_map.deleteMarker(key)
                    self.drone_markers_dict = {}
                elif obj == 'paths':
                    for key in self.drone_paths_dict.keys():
                        self.rescue_map.deletePolyLine(key)
                        self.ovv_map.deletePolyLine(key)
                    self.drone_paths_dict = {}
                elif obj == 'areas':
                    for key in self.drone_areas_dict.keys():
                        self.rescue_map.deletePolygon(key)
                        self.ovv_map.deletePolygon(key)
                    self.drone_areas_dict = {}
                elif obj == 'drones':
                    for key in self.drone_initial_positions.keys():
                        self.rescue_map.deleteMarker(key)
                        self.ovv_map.deleteMarker(key)
                    self.drone_initial_positions = {}
            
            return
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Error: {repr(e)}, try to modify the grid size or number of areas",
                src_msg="Remove objects",
                type_msg="error",
            )

    def show_drones(self, init=True) -> None:
        """Show the drones on the map"""
        # TODO: if init show the point, if not, show the current position from files
        self.drone_position_list = []
        self.drone_station_position = None
        
        for key in self.drone_initial_positions.keys():
            self.rescue_map.deleteMarker(key)
            self.ovv_map.deleteMarker(key)
        self.drone_initial_positions = {}

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
                self.drone_initial_positions["uav_" + str(i + 1)] = (lat, lon)
        # assign the first drone as the station
        self.drone_station_position = self.drone_position_list[0]

    def show_geodata(self, geodata: dict) -> None:
        # Show the points on the rescue map

        for ind, (lat, lon) in enumerate(geodata["Points"]):
            self.rescue_map.addMarker(
                "Marker" + str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(dot_icon_path), iconSize={"width": 10, "height": 10}),
            )
            self.ovv_map.addMarker(
                "Marker" + str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(dot_icon_path), iconSize={"width": 10, "height": 10}),
            )
            if self.debug:
                print(f"Added marker {ind} at {lat}, {lon}")

        # Show the line on the rescue map
        for ind, (start, end) in enumerate(geodata["LineString"]):

            self.rescue_map.drawPolyLine(
                "Line" + str(ind), [start, end], options=dict(color="yellow", weight=5)
            )
            self.ovv_map.drawPolyLine(
                "Line" + str(ind), [start, end], options=dict(color="yellow", weight=5)
            )
            if self.debug:
                print(f"Added line {ind} from {start} to {end}")

        # Show the polygon on the rescue map
        for ind, polygon in enumerate(geodata["Polygon"]):
            self.rescue_map.drawPolygon(
                "Area" + str(ind),
                polygon,
                options=dict(
                    color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2
                ),
            )
            self.ovv_map.drawPolygon(
                "Area" + str(ind),
                polygon,
                options=dict(
                    color="green", weight=2, fill=True, fillColor="green", fillOpacity=0.2
                ),
            )
            
            if self.debug:
                print(f"Added polygon {ind} with points {polygon}")
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
    run()
