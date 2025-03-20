# !/usr/bin/env python3
import copy
import pprint
import sys
from datetime import datetime
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

# Set timezone for Vietnam
vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
CURRENT_TIME = datetime.now(vietnam_tz)
PARENT_DIR = Path(__file__).parent.parent

# cspell: ignore Minh qtwebchannel geocoder asyncio, asyncqt, geojson, geojsons, html, htm, lon, lat, lst, uav, uavs, uav_index, uav_indexs

# Define the path to the icons
DRONE_ICON_PATH = "../assets/icons/drone.png"
DOT_ICON_PATH = "../assets/icons/red_dot.png"

"""
MAP FUNCTIONALITY NOTES:

Main map (leaflet.js):
- Interactive map that allows drawing points, lines, and polygons
- Exports data as GeoJSON (saved to files and sent via qtwebchannel)
- Supports adding markers, lines, and polygons from GeoJSON data

Overview map (leaflet.js):
- One-way display from Python to HTML
- Shows points, lines, and polygons from GeoJSON data
- Non-interactive mirror of the main map
"""


class Map(Interface):
    """
    Map class for the UAV control interface
    
    This class extends the base Interface to provide mapping and mission planning
    capabilities for UAV operations, including area splitting, grid generation,
    route planning, and visualization.
    
    Attributes:
        debug (bool): Enable/disable debug print statements
        noArea (int): Number of areas to split the polygon into
        drone_num (int): Number of drones available
        gridSize (int): Grid spacing in meters
    """

    debug = False

    # Map configuration parameters
    noArea = 5
    drone_num = 5
    gridSize = 10  # meters

    # State tracking
    drone_path_enabled = False
    reduced_grid_points = False
    refreshed = False
    
    # Data storage
    geodata = {}
    drone_areas_dict = {}
    drone_paths_dict = {}
    drone_markers_dict = {}
    drone_initial_positions = {}

    def __init__(self):
        """Initialize the map interface"""
        Interface.__init__(self)
        self._init_map()
        self._init_map_events()

    def _init_map(self):
        """Initialize map components and default settings"""
        try:
            # Set tab to map view
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(0)

            # Initialize Rescue Map (main interactive map)
            self.rescue_map = MapEngine(
                name="Rescue Map", widget=self.ui.MapWebView, url=map_html_path
            )
            self._setup_map_callbacks(self.rescue_map)
            self.rescue_map.setZoom(30)
            self.rescue_map.waitUntilReady()

            # Initialize Overview Map (non-interactive mirror)
            self.ovv_map = MapEngine(
                name="Overview Map",
                widget=self.ui.Overview_map_view,
                url=map_ovv_html_path,
            )
            self.ovv_map.mapMovedCallback = self.onMapOvvMoved
            self.ovv_map.waitUntilReady()

            # Set initial values in UI
            self.ui.noArea_line_edit.setText(str(self.noArea))
            self.ui.gridSize_line_edit.setText(str(self.gridSize))
            self.ui.dateTimeEdit.setDateTime(CURRENT_TIME)

            # Show drones on the map
            self.show_drones()
            
        except Exception as e:
            logger.error(f"Failed to initialize map: {e}")
            self.popup_msg(
                f"Error initializing map: {e}",
                src_msg="_init_map",
                type_msg="error"
            )
            
    def _setup_map_callbacks(self, map_engine):
        """Set up callbacks for a map engine instance
        
        Args:
            map_engine: The MapEngine instance to configure
        """
        # Map event callbacks
        map_engine.mapMovedCallback = self.onMapMoved
        map_engine.mapClickedCallback = self.onMapLClick
        map_engine.mapDoubleClickedCallback = self.onMapDClick
        map_engine.mapRightClickedCallback = self.onMapRClick

        # Marker event callbacks
        map_engine.markerMovedCallback = self.onMarkerMoved
        map_engine.markerClickedCallback = self.onMarkerLClick
        map_engine.markerDoubleClickedCallback = self.onMarkerDClick
        map_engine.markerRightClickedCallback = self.onMarkerRClick

        # GeoJSON callback
        map_engine.mapGeojsonCallback = self.onMapGeojson
        
    def _init_map_events(self):
        """
        Initialize map event handlers by connecting UI buttons and inputs
        to their respective callback functions
        """
        try:
            # Connect buttons to callbacks
            button_callbacks = {
                self.ui.btn_map_create_routes: self.btn_map_create_routes_callback,
                self.ui.btn_map_show_grid_points: self.btn_map_show_grid_points_callback,
                self.ui.btn_map_refresh_data: self.btn_refresh_data_callback,
                self.ui.btn_map_export_plan: self.btn_map_export_plan_callback,
                self.ui.btn_map_split_area: self.btn_split_area_callback,
                self.ui.btn_map_reduce_points: self.btn_map_reduce_points_callback,
                self.ui.btn_map_toggle_route: self.btn_toggle_route_callback,
            }
            
            for button, callback in button_callbacks.items():
                button.clicked.connect(callback)

            # Connect line edits to callbacks
            self.ui.noArea_line_edit.returnPressed.connect(self.noArea_line_edit_callback)
            self.ui.gridSize_line_edit.returnPressed.connect(self.gridSize_line_edit_callback)
    
        except Exception as e:
            logger.error(f"Failed to initialize map events: {e}")
            self.popup_msg(
                f"Error setting up map event handlers: {e}",
                src_msg="_init_map_events",
                type_msg="error"
            )
    # ------------------------ Map Button Event Handlers ------------------------

    def btn_map_create_routes_callback(self):
        """
        Create or remove flight routes connecting grid points for each drone
        
        This function toggles the display of path lines between grid points,
        with each area having a different color path.
        """
        if self.debug:
            print("Button clicked: Create routes")

        try:
            colors = ["red", "blue", "green", "yellow", "purple", "orange"]
            
            # If paths are already enabled, remove them
            if self.drone_path_enabled:
                self.remove_objects(["paths"])
                self.drone_paths_dict = {}
                self.drone_path_enabled = False
                return
                
            # Otherwise, create and display paths
            self.drone_path_enabled = True
            self.drone_paths_dict = {}

            # Group grid points by area
            area_grid_points = {}
            for key, value in self.drone_markers_dict.items():
                area_index = int(key.split("A")[1].split("P")[0])
                point_index = int(key.split("P")[1])
                area_grid_points.setdefault(area_index, []).append(value)

            # Create paths for each area with a different color
            for ind, (_, value) in enumerate(area_grid_points.items()):
                color = colors[ind % len(colors)]

                # First path: from drone to first grid point
                start = self.drone_position_list[ind]
                end = value[0]

                path_key = f"A{ind + 1}P{0}-{1}"
                self.rescue_map.drawPolyLine(
                    path_key, [start, end], options=dict(color=color, weight=5)
                )
                self.ovv_map.drawPolyLine(
                    path_key, [start, end], options=dict(color=color, weight=5)
                )
                self.drone_paths_dict[path_key] = (start, end)

                # Connect all remaining points in sequence
                for j in range(1, len(value)):
                    start = value[j - 1]
                    end = value[j]
                    path_key = f"A{ind + 1}P{j}-{j + 1}"
                    
                    self.rescue_map.drawPolyLine(
                        path_key, [start, end], options=dict(color=color, weight=5)
                    )
                    self.ovv_map.drawPolyLine(
                        path_key, [start, end], options=dict(color=color, weight=5)
                    )
                    self.drone_paths_dict[path_key] = (start, end)
                    
        except Exception as e:
            logger.error(f"Failed to create routes: {e}")
            self.popup_msg(
                f"Error creating routes: {e}",
                src_msg="Create routes",
                type_msg="error"
            )

    def btn_map_show_grid_points_callback(self):
        """
        Generate and display grid points within the defined area
        
        This function:
        1. Creates a grid of points within the selected polygon
        2. Displays these points on both the main and overview maps
        3. Exports the points to files for mission planning
        """
        if self.debug:
            print("Button clicked: Show grid points")

        try:
            grid_size = self.gridSize
            n_areas = min(self.noArea, self.drone_num)

            # Validate parameters
            if grid_size <= 0 or n_areas <= 0:
                logger.error("Invalid grid size or number of areas")
                self.popup_msg(
                    "Grid size and number of areas must be positive",
                    src_msg="Show grid points",
                    type_msg="error"
                )
                return

            # If grid points already exist and were previously reduced/refreshed, just display them
            if (self.reduced_grid_points or self.refreshed) and self.drone_markers_dict:
                self._redisplay_grid_points()
                return

            # Generate new grid points by splitting the area
            grid_points = split_grids(self.rotated_area_list, *self.extra, grid_size, n_areas)

            # Update state
            self.multi_area = n_areas > 1
            
            # Clear existing markers and prepare for new ones
            self.remove_objects(["markers"])
            self.drone_markers_dict = {}

            # Process and display the grid points
            self.process_grid_points(grid_points)
            self.grid_enabled = True

        except Exception as e:
            logger.error(f"Failed to generate grid points: {e}")
            self.popup_msg(
                f"Error generating grid points: {e}\nTry modifying the grid size or number of areas",
                src_msg="Show grid points",
                type_msg="error"
            )
            
    def _redisplay_grid_points(self):
        """Redisplay existing grid points on the map"""
        self.remove_objects(["markers"])
        
        marker_options = {
            "icon": str(DOT_ICON_PATH), 
            "iconSize": {"width": 5, "height": 5}
        }
        
        for key, value in self.drone_markers_dict.items():
            self.rescue_map.addMarker(key, float(value[0]), float(value[1]), **marker_options)
            self.ovv_map.addMarker(key, float(value[0]), float(value[1]), **marker_options)

            
    def process_grid_points(self, grid_points):
        """
        Process and display grid points on the map
        
        Args:
            grid_points: List of grid points for each area
        """
        try:
            # Reset state flags
            self.reduced_grid_points = False
            self.refreshed = False
            
            marker_options = {
                "icon": str(DOT_ICON_PATH), 
                "iconSize": {"width": 5, "height": 5}
            }

            if self.multi_area:
                # Process each area separately
                for ind, area in enumerate(grid_points):
                    self._process_single_area(area, ind + 1, marker_options)
            else:
                # Process single area
                self._process_single_area(grid_points, 1, marker_options)

        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Error: {repr(e)}, try to modify the grid size or number of areas",
                src_msg="Process grid points",
                type_msg="error",
            )
            
    def _process_single_area(self, area_points, area_index, marker_options):
        """Process and display grid points for a single area"""
        # Find optimal path through points
        ordered_points = find_path(area_points, self.drone_position_list[0])
        ordered_points = remove_duplicate_pts(ordered_points)

        # Check if there are too many points
        if len(ordered_points) > 100:
            logger.log("Too many points to plot, try to increase grid size!", level="warning")
            return

        # Add markers for each point
        for i, point in enumerate(ordered_points):
            marker_id = f"A{area_index}P{i + 1}"
            self.rescue_map.addMarker(marker_id, float(point[0]), float(point[1]), **marker_options)
            self.ovv_map.addMarker(marker_id, float(point[0]), float(point[1]), **marker_options)
            self.drone_markers_dict[marker_id] = point

        # Save points to file
        with open(f"{PARENT_DIR}/src/logs/points/points{area_index}.txt", "w") as file:
            for lat, lon in ordered_points:
                file.write(f"{lat}, {lon}\n")

    def btn_refresh_data_callback(self):
        """
        Load map data from a saved JSON file and update the display
        
        This lets users restore a previously saved mission plan.
        """
        if self.debug:
            print("Button clicked: Refresh data")

        try:
            # Open file dialog to select a JSON file
            filename = QFileDialog.getOpenFileName(
                parent=self,
                caption="Open map file",
                directory=f"{PARENT_DIR}/src/logs/",
                initialFilter="Files (*.json)"
            )[0]
            
            if not filename:
                logger.warning("No file selected, plotting default grid")
                return
                
            # Load the JSON data
            with open(filename, "r") as file:
                data = json.load(file)
                
            # Update the local data structures
            self.geodata["Polygon"] = data.get("Area", [])
            self.geodata["Points"] = data.get("Points", [])
            self.geodata["LineString"] = data.get("LineString", [])
            self.drone_areas_dict = data.get("Drone areas:", {})
            self.drone_markers_dict = data.get("Drone grid points", {})
            self.drone_paths_dict = data.get("Drone paths", {})

            logger.info(f"Updated data from file: {filename}")
            self.popup_msg(
                "Data updated successfully, please re-process",
                src_msg="Refresh data",
                type_msg="info"
            )
            self.refreshed = True

        except Exception as e:
            logger.error(f"Failed to refresh data: {e}")
            self.popup_msg(
                f"Error refreshing map data: {e}",
                src_msg="Refresh data",
                type_msg="error"
            )

    def btn_map_export_plan_callback(self, to_plan_format=False):
        """
        Export the current mission plan to a JSON file
        
        Args:
            to_plan_format: If True, export in QGroundControl .plan format (Not implemented)
        """
        if self.debug:
            print("Button clicked: Export plan")

        try:
            if to_plan_format:
                # TODO: Implement QGroundControl .plan format export
                logger.warning("Exporting to QGroundControl .plan format is not implemented")
                return
            
            # Create timestamp for filename
            timestamp = CURRENT_TIME.strftime('%Y-%m-%d_%H-%M-%S')
            file_path = f"{PARENT_DIR}/src/logs/map_data/map_runtime_{timestamp}.json"

            # Prepare data for export
            data = {
                "Area": self.geodata.get("Polygon", []),
                "Points": self.geodata.get("Points", []),
                "LineString": self.geodata.get("LineString", []),
                "Drone areas:": {key: area for key, area in self.drone_areas_dict.items()},
                "Drone grid points": {key: value for key, value in self.drone_markers_dict.items()},
                "Drone paths": {key: value for key, value in self.drone_paths_dict.items()},
            }

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write to file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            logger.info(f"Exported data to {file_path}")
            self.popup_msg(
                f"Exported data to {file_path}",
                src_msg="Export plan",
                type_msg="info"
            )

        except Exception as e:
            logger.error(f"Failed to export plan: {e}")
            self.popup_msg(
                f"Error exporting plan: {e}",
                src_msg="Export plan",
                type_msg="error"
            )

    def btn_split_area_callback(self):
        """
        Split a polygon area into multiple sub-areas for multi-drone missions
        
        This divides the drawn polygon into roughly equal parts based on the
        number of drones/areas specified.
        """
        if self.debug:
            print("Button clicked: Split area")

        try:
            # Validate polygon data
            if not self.geodata.get("Polygon"):
                logger.error("No polygon data to split")
                self.popup_msg(
                    "No polygon data to split. Draw a polygon first.",
                    src_msg="Split area",
                    type_msg="error"
                )
                return

            # Get polygon points
            polygon_points = self.geodata["Polygon"][0]
            if len(polygon_points) < 3:
                logger.error(f"Invalid polygon: {polygon_points}")
                self.popup_msg(
                    "Invalid polygon. Need at least 3 points.",
                    src_msg="Split area",
                    type_msg="error"
                )
                return

            if self.debug:
                print("Polygon points:", polygon_points)

            # Clear existing objects
            self.remove_objects(["markers", "paths", "areas"])
            self.drone_areas_dict = {}

            # Split the polygon
            n_areas = min(self.noArea, self.drone_num)
            logger.info(f"Splitting area into {n_areas} parts")
            
            splitted_areas, rotated_area_list, angle, midpoint, min_lat, min_lon = (
                split_polygon_into_areas_old(polygon_points, n_areas)
            )

            # Draw the split areas on the map
            for ind, area in enumerate(splitted_areas):
                if self.debug:
                    print(f"Area {ind}: {area}")

                # Ensure polygon is closed
                if area[0] != area[-1]:
                    area.append(area[0])

                # Draw on both maps
                key = f"Area_{ind}"
                area_options = dict(
                    color="blue", 
                    weight=2, 
                    fill=True, 
                    fillColor="blue", 
                    fillOpacity=0.2
                )
                
                self.rescue_map.drawPolygon(key=key, coordinates=area, options=area_options)
                self.ovv_map.drawPolygon(key=key, coordinates=area, options=area_options)
                self.drone_areas_dict[key] = area

                # Save area to file
                area_file = f"{PARENT_DIR}/src/logs/area/area{ind + 1}.txt"
                with open(area_file, "w") as file:
                    for lat, lon in area:
                        file.write(f"{lat}, {lon}\n")

            # Store for later use
            self.rotated_area_list = rotated_area_list
            self.extra = (angle, midpoint, min_lat, min_lon)

        except Exception as e:
            logger.error(f"Failed to split area: {e}")
            self.popup_msg(
                f"Error splitting area: {e}",
                src_msg="Split area",
                type_msg="error"
            )

    def btn_map_reduce_points_callback(self):
        """
        Reduce the number of grid points by removing unnecessary intermediate points
        
        This simplifies the mission by removing grid points that lie on straight lines,
        keeping only the endpoints and points where direction changes.
        """
        if self.debug:
            print("Button clicked: Reduce points")

        try:
            # Group grid points by area
            area_grid_points = {}
            for key, value in self.drone_markers_dict.items():
                area_index = int(key.split("A")[1].split("P")[0])
                point_index = int(key.split("P")[1])
                area_grid_points.setdefault(area_index, []).append(value)

            # Remove existing markers
            self.remove_objects(["markers"])
            self.drone_markers_dict = {}
            reduced_grid_point_list = []

            # Process each area
            for ind, points_in_area in enumerate(area_grid_points.values()):
                # Skip areas with too few points
                if len(points_in_area) < 3:
                    reduced_grid_point_list.append(points_in_area)
                    continue

                # Keep endpoints and points where direction changes
                filtered_points = [points_in_area[0]]
                i = 1
                while i < len(points_in_area) - 1:
                    if point_on_line(
                        points_in_area[i - 1], points_in_area[i], points_in_area[i + 1]
                    ):
                        # Skip points that lie on straight lines
                        i += 1
                    else:
                        # Keep points where direction changes
                        filtered_points.append(points_in_area[i])
                        i += 1
                        
                # Always keep the last point
                filtered_points.append(points_in_area[-1])

                # Add markers for the filtered points
                for i, point in enumerate(filtered_points):
                    marker_key = f"A{ind + 1}P{i + 1}"
                    self.rescue_map.addMarker(
                        marker_key,
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(DOT_ICON_PATH), iconSize={"width": 5, "height": 5})
                    )
                    self.ovv_map.addMarker(
                        marker_key,
                        float(point[0]),
                        float(point[1]),
                        **dict(icon=str(DOT_ICON_PATH), iconSize={"width": 5, "height": 5})
                    )
                    self.drone_markers_dict[marker_key] = point

                reduced_grid_point_list.append(filtered_points)
                
            # Save filtered points to files
            for i, points in enumerate(reduced_grid_point_list):
                points_file = f"{PARENT_DIR}/src/logs/points/reduced_point{i + 1}.txt"
                with open(points_file, "w") as file:
                    for lat, lon in points:
                        file.write(f"{lat}, {lon}\n")
                        
            self.reduced_grid_points = True
            logger.info("Successfully reduced grid points")

        except Exception as e:
            logger.error(f"Failed to reduce points: {e}")
            self.popup_msg(
                f"Error reducing points: {e}",
                src_msg="Reduce points",
                type_msg="error"
            )

    def btn_toggle_route_callback(self):
        """Toggle between showing grid points and showing routes"""
        if self.debug:
            print("Button clicked: Toggle route")

        try:
            # Simply call the grid points and routes functions in sequence
            self.btn_map_show_grid_points_callback()
            self.btn_map_create_routes_callback()
        except Exception as e:
            logger.error(f"Failed to toggle route: {e}")
            self.popup_msg(
                f"Error toggling route display: {e}",
                src_msg="Toggle route",
                type_msg="error"
            )

    def noArea_line_edit_callback(self):
        """Update the number of areas parameter from the UI input"""
        try:
            value = self.ui.noArea_line_edit.text().strip()
            new_value = int(value)
            if new_value <= 0:
                raise ValueError("Number of areas must be positive")
                
            self.noArea = new_value
            logger.info(f"Set number of areas to: {self.noArea}")
            
            # Reset states since parameters changed
            self.refreshed = False
            self.reduced_grid_points = False
            
        except ValueError as e:
            logger.error(f"Invalid value for number of areas: {e}")
            self.popup_msg(
                f"Invalid value: {value}. Number of areas must be a positive integer.",
                src_msg="Set number of areas",
                type_msg="error"
            )
            # Reset to previous value
            self.ui.noArea_line_edit.setText(str(self.noArea))

    def gridSize_line_edit_callback(self):
        """Update the grid size parameter from the UI input"""
        try:
            value = self.ui.gridSize_line_edit.text().strip()
            new_value = int(value)
            if new_value <= 0:
                raise ValueError("Grid size must be positive")
                
            self.gridSize = new_value
            logger.info(f"Set grid size to: {self.gridSize}")
            
            # Reset states since parameters changed
            self.refreshed = False
            self.reduced_grid_points = False
            
        except ValueError as e:
            logger.error(f"Invalid value for grid size: {e}")
            self.popup_msg(
                f"Invalid value: {value}. Grid size must be a positive integer.",
                src_msg="Set grid size",
                type_msg="error"
            )
            # Reset to previous value
            self.ui.gridSize_line_edit.setText(str(self.gridSize))

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
    def onMapGeojson(self, json_data) -> None:
        """
        Handles the GeoJSON data and updates the map accordingly.
        Parameters:
        json_data (dict): The GeoJSON data to be processed.
        The function processes the GeoJSON data to extract coordinates and type of geometry.
        Depending on the type of geometry (Point, Polygon, LineString), it performs the following actions:
        - For Point: Adds a marker to the map and appends the position to the position list.
        - For Polygon: Calculates the area, updates the area label, displays the polygon on the map, and exports the coordinates to a file.
        - For LineString: Draws a polyLine on the map.
        The function also logs any exceptions that occur during processing.
        """

        try:
            coordinates = geojson_to_coordinates(json_data)
            type_name, points = coordinates

            # Clear previous data of this type
            self.geodata.setdefault(type_name, []).clear()
            self.remove_objects(["markers", "paths", "areas"])
            
            if type_name == "Point":
                lon, lat = points
                self.ovv_map.deleteMarker(type_name)
                self.ovv_map.addMarker("Point", lat, lon, icon=DOT_ICON_PATH)

            elif type_name == "LineString":
                points = [[float(lat), float(lon)] for lon, lat in points]
                self.ovv_map.deletePolyLine(type_name)
                self.ovv_map.drawPolyLine(type_name, points)

            elif type_name == "Polygon":
                points = [[float(lat), float(lon)] for lon, lat in points[0]]

                # Calculate and display the area
                area = area_of_polygon(points)
                self.ui.area_value.setText(f"{round(area['ha'], 2)} ha")

                # Display on overview map
                self.ovv_map.deletePolygon(type_name)
                self.ovv_map.drawPolygon(type_name, points)

            # Store the data
            self.geodata.setdefault(type_name, []).append(points)
            
            # Reset state flags
            self.refreshed = False
            self.reduced_grid_points = False           

        except Exception as e:
            logger.log(repr(e), level="error")
            
    def remove_objects(self, object_types):
        """Remove objects of specified types from both maps"""
        if self.debug:
            print("Removing objects:", object_types)
            
        if not object_types:
            return
            
        try:
            for obj_type in object_types:
                if obj_type == 'markers' and self.drone_markers_dict:
                    for key in self.drone_markers_dict:
                        self.rescue_map.deleteMarker(key)
                        self.ovv_map.deleteMarker(key)
                    self.drone_markers_dict = {}
                    
                elif obj_type == 'paths' and self.drone_paths_dict:
                    for key in self.drone_paths_dict:
                        self.rescue_map.deletePolyLine(key)
                        self.ovv_map.deletePolyLine(key)
                    self.drone_paths_dict = {}
                    
                elif obj_type == 'areas' and self.drone_areas_dict:
                    for key in self.drone_areas_dict:
                        self.rescue_map.deletePolygon(key)
                        self.ovv_map.deletePolygon(key)
                    self.drone_areas_dict = {}
                    
                elif obj_type == 'drones' and self.drone_initial_positions:
                    for key in self.drone_initial_positions:
                        self.rescue_map.deleteMarker(key)
                        self.ovv_map.deleteMarker(key)
                    self.drone_initial_positions = {}
                    
        except Exception as e:
            logger.log(repr(e), level="error")
            self.popup_msg(
                f"Error removing objects: {repr(e)}",
                src_msg="Remove objects",
                type_msg="error",
            )

    def show_drones(self, init=True) -> None:
        """
        Show drone markers on the map
        
        Args:
            init: If True, show drones at their initial positions from drone_init_pos
                If False, show drones at their current positions from drone_current_pos
        """
        try:
            # Clear previous drone markers
            self.remove_drone_markers()
            
            # Reset position lists
            self.drone_position_list = []
            self.drone_station_position = None
            
            # Set the position source directory based on init flag
            position_dir = (
                f"{PARENT_DIR}/src/logs/drone_init_pos" if init else
                f"{PARENT_DIR}/src/logs/drone_current_pos"
            )
            
            # Track which drones have been successfully loaded
            loaded_drones = 0
            
            # Load positions for each drone
            for i in range(self.drone_num):
                drone_id = i + 1
                position_file = f"{position_dir}/uav_{drone_id}.txt"
                
                try:
                    # Read position from file
                    if os.path.exists(position_file):
                        with open(position_file, "r") as file:
                            line = file.readline().strip()
                            if line:
                                lat, lon = map(float, line.split(","))
                                
                                # Add to position list
                                self.drone_position_list.append((lat, lon))
                                
                                # Create marker options
                                marker_options = {
                                    "icon": DRONE_ICON_PATH,
                                    "draggable": False,
                                    "title": f"UAV {drone_id}",
                                    "iconSize": {"width": 21, "height": 21},
                                }
                                
                                # Add marker to both maps
                                marker_key = f"uav_{drone_id}"
                                self.rescue_map.addMarker(
                                    key=marker_key,
                                    latitude=lat,
                                    longitude=lon,
                                    **marker_options
                                )
                                self.ovv_map.addMarker(
                                    key=marker_key,
                                    latitude=lat,
                                    longitude=lon,
                                    **marker_options
                                )
                                
                                # Store position
                                self.drone_initial_positions[marker_key] = (lat, lon)
                                loaded_drones += 1
                                
                                if self.debug:
                                    print(f"Loaded {marker_key} position: {lat}, {lon}")
                    else:
                        # If file doesn't exist for current positions, try to use initial position
                        if not init:
                            init_position_file = f"{PARENT_DIR}/src/logs/drone_init_pos/uav_{drone_id}.txt"
                            if os.path.exists(init_position_file):
                                with open(init_position_file, "r") as file:
                                    lat, lon = map(float, file.readline().strip().split(","))
                                    logger.warning(f"Current position not found for UAV {drone_id}, using initial position")
                            else:
                                # Use default position if neither file exists
                                lat, lon = (INIT_LAT + 0.0001 * i, INIT_LON + 0.0001 * i)
                                logger.warning(f"No position data found for UAV {drone_id}, using default position")
                            
                            # Add this fallback position
                            self.drone_position_list.append((lat, lon))
                            marker_key = f"uav_{drone_id}"
                            marker_options = {
                                "icon": DRONE_ICON_PATH,
                                "draggable": False,
                                "title": f"UAV {drone_id} (Default)",
                                "iconSize": {"width": 21, "height": 21},
                            }
                            self.rescue_map.addMarker(key=marker_key, latitude=lat, longitude=lon, **marker_options)
                            self.ovv_map.addMarker(key=marker_key, latitude=lat, longitude=lon, **marker_options)
                            self.drone_initial_positions[marker_key] = (lat, lon)
                            loaded_drones += 1
                
                except Exception as e:
                    logger.error(f"Failed to load position for UAV {drone_id}: {e}")
            
            # Make sure we have at least one drone position
            if not self.drone_position_list:
                # Use default position if no drones were loaded
                default_lat, default_lon = INIT_LAT, INIT_LON
                self.drone_position_list.append((default_lat, default_lon))
                marker_key = "uav_default"
                marker_options = {
                    "icon": DRONE_ICON_PATH,
                    "draggable": False,
                    "title": "Default UAV Position",
                    "iconSize": {"width": 21, "height": 21},
                }
                self.rescue_map.addMarker(key=marker_key, latitude=default_lat, longitude=default_lon, **marker_options)
                self.ovv_map.addMarker(key=marker_key, latitude=default_lat, longitude=default_lon, **marker_options)
                self.drone_initial_positions[marker_key] = (default_lat, default_lon)
                logger.warning("Using default drone position since no positions were loaded")
            
            # Set the first drone as the station
            self.drone_station_position = self.drone_position_list[0]
            
            # Center map on first drone if needed
            if loaded_drones > 0:
                first_pos = self.drone_position_list[0]
                self.rescue_map.centerAt(first_pos[0], first_pos[1])
                self.ovv_map.centerAt(first_pos[0], first_pos[1])
            
            if self.debug:
                print(f"Loaded {loaded_drones} drone positions, using {'initial' if init else 'current'} positions")
        
        except Exception as e:
            logger.error(f"Error showing drones: {e}")
            self.popup_msg(
                f"Error showing drones: {e}",
                src_msg="Show drones",
                type_msg="error"
            )

    def remove_drone_markers(self):
        """Remove all drone markers from the map"""
        if self.drone_initial_positions:
            for key in self.drone_initial_positions.keys():
                self.rescue_map.deleteMarker(key)
                self.ovv_map.deleteMarker(key)
            self.drone_initial_positions = {}

    def update_drone_positions(self):
        """
        Update drone positions on the map in real-time
        
        This function reads current drone positions and updates the map markers.
        It's designed to be called periodically to reflect live position changes.
        """
        self.show_drones(init=False)

    def show_geodata(self, geodata: dict) -> None:
        # Show the points on the rescue map

        for ind, (lat, lon) in enumerate(geodata["Points"]):
            self.rescue_map.addMarker(
                "Marker" + str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(DOT_ICON_PATH), iconSize={"width": 10, "height": 10}),
            )
            self.ovv_map.addMarker(
                "Marker" + str(ind),
                float(lat),
                float(lon),
                **dict(icon=str(DOT_ICON_PATH), iconSize={"width": 10, "height": 10}),
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

