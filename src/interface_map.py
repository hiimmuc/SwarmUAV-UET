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
from PyQt5.QtCore import QTimer

from pathlib import Path
from map.chuongtrinhcon_newUI import *
# from interface_wrapper import UAVs

parent_dir = Path(__file__).parent.parent



# Define the path to the assets/icons directory
ICON_DIR = Path(__file__).parent.parent / 'assets' / 'icons'
drone_icon_path = ICON_DIR / 'drone.png'
dot_icon_path = ICON_DIR / 'Dot.png'

rotated_area_list = []
grid_enabled = False
grid_points = []
final_grid = []

class Map(Interface):
    position_list = []  # This is a class attribute
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
        # Initialize the timer and set update flag
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self.update_uav_positions)
        self._updating_positions = False  # Flag to track if updates are active


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
        # Toggle update status
        if not self._updating_positions:
            # Start updates if they are not already running
            self.start_uav_updates()
        else:
            # Stop updates if they are currently running
            self.stop_uav_updates()

    def start_uav_updates(self):
        # Start the timer to update every 1 second
        self._update_timer.start(1000)
        self._updating_positions = True  # Set flag to indicate updates are active

    def stop_uav_updates(self):
        # Stop the timer and set flag to indicate updates are inactive
        self._update_timer.stop()
        self._updating_positions = False


    def update_uav_positions(self):
        # Get GPS data from drones' gps.log file and update positions
        from interface_wrapper import UAVs  # Local import to avoid circular dependency

        # Generate JavaScript code to update each UAV's position
        js_code = ""
        for uav_index in range(1, 7):
            if UAVs[uav_index]["status"]["connection_status"]:
                latitude = UAVs[uav_index]["status"]["position_status"][0]
                longitude = UAVs[uav_index]["status"]["position_status"][1]
                if latitude != "No information" and longitude != "No information":
                    # Call updateUAVMarker function in JavaScript
                    js_code += f"updateUAVMarker({uav_index}, {latitude}, {longitude});"
        
        # Execute the generated JavaScript code to update UAV markers on the map
        self.ui.MapWebView.page().runJavaScript(js_code)

    # def btn_show_drones_callback(self):
    #     # get gps from drones gps.log file and show on map
    #     from interface_wrapper import UAVs  # Local import to avoid circular dependency
    #     # Generate JavaScript code to update each UAV's position
    #     js_code = ""
    #     for uav_index in range(1, 7):
    #         if UAVs[uav_index]["status"]["connection_status"]:
    #             latitude = UAVs[uav_index]["status"]["position_status"][0]
    #             longitude = UAVs[uav_index]["status"]["position_status"][1]
    #             if latitude != "No information" and longitude != "No information":
    #                 # Call updateUAVMarker function in JavaScript
    #                 js_code += f"updateUAVMarker({uav_index}, {latitude}, {longitude});"
    #                 # Display the UAV's position on the map
    #                 html = self.ovv_map_data.add_marker("Point", float(latitude), float(longitude),
    #                     icon={"icon_path": drone_icon_path}
    #                 )
    #                 # Update the map view with the new marker
    #                 # self.ui.Overview_map_view.setHtml(html)
    #     # Execute the generated JavaScript code
    #     self.ui.MapWebView.page().runJavaScript(js_code)

    def btn_show_points_callback(self):
        # read points from file and show on map
        # Read and parse the JSON file
        filename = filedialog.askopenfilename(initialdir=f"{parent_dir}/logs/area/", title="Chọn file",
                                              filetypes=(("Text files", "*.plan"), ("All files", "*.*")))
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # Initialize an empty list to store (latitude, longitude) tuples
        position_file_list = []

        # Access the mission items to retrieve coordinates
        items = data.get('mission', {}).get('items', [])

        for item in items:
            # Extract latitude and longitude from the params field
            params = item.get('params', [])
            if len(params) >= 6:  # Ensure params has enough elements
                latitude, longitude = params[4], params[5]  # Fifth and sixth elements
                if latitude is not None and longitude is not None and (latitude, longitude) != (0, 0):
                    position_file_list.append([latitude, longitude])
                    self.position_list.append([latitude, longitude])


        # NOTE: draw to ui - positions_list
        # Draw each position on the map
        for latitude, longitude in position_file_list:
            # Assuming `type` is "Point" for all markers
            html = self.ovv_map_data.add_marker(
                "Point", float(latitude), float(longitude), icon={"color": "blue", "icon": "map-pin"}
            )
            self.ui.Overview_map_view.setHtml(html)
        print(self.position_list)

    def btn_refresh_data_callback(self):
        # read points from map interface and update to database
        pass

    def btn_export_points_callback(self):
        # export points to file
        # Define the structure of the .plan file according to QGroundControl specifications
        plan_data = {
            "fileType": "Plan",
            "geoFence": {
                "circles": [],
                "polygons": [],
                "version": 2
            },
            "groundStation": "QGroundControl",
            "mission": {
                "cruiseSpeed": 2,  # Set cruise speed in m/s
                "hoverSpeed": None,    # Set hover speed in m/s
                "firmwareType": 12, # Specify the firmware type (e.g., PX4)
                "globalPlanAltitudeMode": 1,  # Altitude mode
                "items": [],
                "plannedHomePosition": [0, 0, 0],  # Placeholder for home position
                "vehicleType": 2,  # Type of vehicle (e.g., 2 for fixed-wing)
                "version": 2
            },
            "rallyPoints": {
                "points": [],  # Initialize with empty points
                "version": 2
            },
            "version": 1
        }

        # Populate mission items from area_grid waypoints
       
        home_position = self.position_list[0]  # First point as the home position
        plan_data["mission"]["plannedHomePosition"] = [home_position[0], home_position[1], None]
        for y, pos in enumerate(self.position_list):
            # First waypoint
            if y == 0:
                waypoint = {
                    "AMSLAltAboveTerrain": None,
                    "Altitude": 3,
                    "AltitudeMode": 1,
                    "autoContinue": True,
                    "command": 22,  # MAV_CMD_NAV_TAKEOFF
                    "doJumpId": y + 1,
                    "frame": 3,
                    "params": [0, 0, 0, None, pos[0], pos[1], 3],
                    "type": "SimpleItem"
                }
                plan_data["mission"]["items"].append(waypoint)
            
            # Last waypoint
            elif y == len(self.position_list) - 1:
                waypoint = {
                    "AMSLAltAboveTerrain": None,
                    "Altitude": 3,
                    "AltitudeMode": 1,
                    "autoContinue": True,
                    "command": 16,  # MAV_CMD_NAV_LAND or equivalent end command
                    "doJumpId": y + 1,
                    "frame": 3,
                    "params": [0, 0, 0, None, pos[0], pos[1], 3],
                    "type": "SimpleItem"
                }
                plan_data["mission"]["items"].append(waypoint)
                waypoint = {
                    "autoContinue": True,
                    "command": 20,  # MAV_CMD_NAV_LAND or equivalent end command
                    "doJumpId": y + 2,
                    "frame": 2,
                    "params": [0, 0, 0, 0, 0, 0, 0],
                    "type": "SimpleItem"
                }
                plan_data["mission"]["items"].append(waypoint)
            
            # Middle waypoints
            else:
                waypoint = {
                    "AMSLAltAboveTerrain": None,
                    "Altitude": 3,
                    "AltitudeMode": 1,
                    "autoContinue": True,
                    "command": 16,  # MAV_CMD_NAV_WAYPOINT
                    "doJumpId": y + 1,
                    "frame": 3,
                    "params": [0, 0, 0, None, pos[0], pos[1], 3],
                    "type": "SimpleItem"
                }
                plan_data["mission"]["items"].append(waypoint)
                
        # Define the path to save the .plan file
        plan_file_path = filedialog.asksaveasfilename(defaultextension=".plan", title="Lưu file",
                                                initialdir=f"{parent_dir}/logs/points/",
                                                filetypes=(("Plan files", "*.plan"), ("All files", "*.*")))

        # Save as JSON to .plan file with UTF-8 encoding
        with open(plan_file_path, 'w', encoding='utf-8') as plan_file:
            json.dump(plan_data, plan_file, indent=4)

        print(f"Mission plan exported to {plan_file_path}")

    def btn_split_area_callback(self):
        # split area to grid
        global rotated_area_list, area_num
        area_num = int(self.ui.noArea_value.toPlainText())
        areas, rotated_area_list = chia_dien_tich(self.position_list, area_num)

        for i, area in enumerate(areas):
            for index, position in enumerate(area):
                area_marker = copy.deepcopy(area)
                html = self.ovv_map_data.add_polygon("Polygon", area_marker)
                self.ui.Overview_map_view.setHtml(html)
                print(
                    f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    def btn_export_grid_callback(self):
        # export grid to file
        global final_grid
        print("Exporting waypoints to .plan file format")
        print(f"{final_grid}")

        # Define the structure of the .plan file according to QGroundControl specifications
        plan_data = {
            "fileType": "Plan",
            "geoFence": {
                "circles": [],
                "polygons": [],
                "version": 2
            },
            "groundStation": "QGroundControl",
            "mission": {
                "cruiseSpeed": 1,  # Set cruise speed in m/s
                "hoverSpeed": 1,    # Set hover speed in m/s
                "firmwareType": 12, # Specify the firmware type (e.g., PX4)
                "globalPlanAltitudeMode": 1,  # Altitude mode
                "items": [],
                "plannedHomePosition": [0, 0, 0],  # Placeholder for home position
                "vehicleType": 2,  # Type of vehicle (e.g., 2 for fixed-wing)
                "version": 2
            },
            "rallyPoints": {
                "points": [],  # Initialize with empty points
                "version": 2
            },
            "version": 1
        }

        # Populate mission items from area_grid waypoints
        for i, points in enumerate(final_grid):
            plan_data["mission"]["items"] = []
            from interface_wrapper import UAVs  # Local import to avoid circular dependency
            uav_index = i+1
            lon, lat  = float(UAVs[uav_index]["status"]["position_status"][0]), float(UAVs[uav_index]["status"]["position_status"][1])
        
            # if area_grid and area_grid[0]:
            #     home_position = area_grid[i][0]  # First point as the home position
            #     plan_data["mission"]["plannedHomePosition"] = [home_position[0], home_position[1], None]
            print("EACH GRID", points)

            if final_grid and final_grid[0]:
                plan_data["mission"]["plannedHomePosition"] = [lon, lat, None]

            for y, pos in enumerate(points):
                # First waypoint
                if y == 0:
                    waypoint = {
                        "AMSLAltAboveTerrain": None,
                        "Altitude": 5 + i,
                        "AltitudeMode": 1,
                        "autoContinue": True,
                        "command": 22,  # MAV_CMD_NAV_TAKEOFF
                        "doJumpId": y + 1,
                        "frame": 3,
                        "params": [0, 0, 0, None, pos[0], pos[1], 5 + i],
                        "type": "SimpleItem"
                    }
                    plan_data["mission"]["items"].append(waypoint)
                
                # Last waypoint
                elif y == len(points) - 1:
                    waypoint = {
                        "AMSLAltAboveTerrain": None,
                        "Altitude": 5 + i,
                        "AltitudeMode": 1,
                        "autoContinue": True,
                        "command": 16,  # MAV_CMD_NAV_LAND or equivalent end command
                        "doJumpId": y + 1,
                        "frame": 3,
                        "params": [0, 0, 0, None, pos[0], pos[1], 5 + i],
                        "type": "SimpleItem"
                    }
                    plan_data["mission"]["items"].append(waypoint)
                    waypoint = {
                        "autoContinue": True,
                        "command": 20,  # MAV_CMD_NAV_LAND or equivalent end command
                        "doJumpId": y + 2,
                        "frame": 2,
                        "params": [0, 0, 0, 0, 0, 0, 0],
                        "type": "SimpleItem"
                    }
                    plan_data["mission"]["items"].append(waypoint)
                
                # Middle waypoints
                else:
                    waypoint = {
                        "AMSLAltAboveTerrain": None,
                        "Altitude": 5 + i,
                        "AltitudeMode": 1,
                        "autoContinue": True,
                        "command": 16,  # MAV_CMD_NAV_WAYPOINT
                        "doJumpId": y + 1,
                        "frame": 3,
                        "params": [0, 0, 0, None, pos[0], pos[1], 5 + i],
                        "type": "SimpleItem"
                    }
                    plan_data["mission"]["items"].append(waypoint)
                    
            # Define the path to save the .plan file
            plan_file_path = f"{parent_dir}/src/logs/points/points{i+1}.plan"

            # Save as JSON to .plan file with UTF-8 encoding
            with open(plan_file_path, 'w', encoding='utf-8') as plan_file:
                json.dump(plan_data, plan_file, indent=4)

            print(f"Mission plan exported to {plan_file_path}")


    def btn_toggle_route_callback(self):
        from interface_wrapper import UAVs  # Local import to avoid circular dependency
        global rotated_area_list, area_num, grid_enabled, grid_points, final_grid
        grid_points = []

        if grid_enabled :
            # # NOTE: If grid is enabled or the number of grid distance have not been inserted -> then clear all the grid marker on map
            # for grid_points_markers in grid_points_markers_list:
            #     for marker in grid_points_markers:
            #         marker.delete()  # Assuming each marker has a delete method
            # # Now clear the lists that were holding the points and markers
            # ordered_grid_points.clear()
            # grid_points_markers_list.clear()
            # area_grid.clear()
            grid_enabled = False
            pass

        else:
            # distance = float(entry_grid_distance.get()) NOTE: take the grid distance
            distance = int(self.ui.noArea_value.toPlainText())
            # Generate new grid points and add markers
            # NOTE: take the number of area from UI
            if area_num in (0, 1):
                position_area = [tuple(lst) for lst in self.position_list]
                grid_points = chia_luoi_one(position_area, distance)
                print("FALSE 2")
            else:
                grid_points = chia_luoi(rotated_area_list, distance)
                print("TRUE")

            # NOTE: path optimization
            area_grid = []
            # NOTE: take UAV 1 Position
            # gps_uav_1 = [21.069963, 105.799692] # example
            gps_uav_1 = UAVs[1]["status"]["position_status"]
            print("GPS UAV1", gps_uav_1)
            area_grid = process_grid_points(grid_points, gps_uav_1)
            
            # NOTE: remove point
            points_sets = copy.deepcopy(area_grid)
            all_filtered_sets = []

            for points in points_sets:
                if len(points) < 3:
                    all_filtered_sets.append(points)
                    continue

                filtered_points = [points[0]]  # Always keep the first point
                i = 1
                while i < len(points) - 1:
                    if point_on_line(points[i - 1], points[i], points[i + 1]):
                        i += 1  # Skip the middle point as it's collinear
                    else:
                        filtered_points.append(points[i])
                        i += 1
                filtered_points.append(points[-1])  # Always keep the last point
                all_filtered_sets.append(filtered_points)

            for grid in all_filtered_sets:
                htm = self.ovv_map_data.add_line("LineString", grid)
                self.ui.Overview_map_view.setHtml(htm)
            
            final_grid = copy.deepcopy(all_filtered_sets)

            # Enable grid
            grid_enabled = True

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
                self.position_list.append((lat, lon))

            elif type == "Polygon":
                self.position_list = []
                points = [[float(lat), float(lon)] for lon, lat in points[0]]
                html = self.ovv_map_data.add_polygon(type, points)
                points.pop()
                self.position_list = copy.deepcopy(points)
                

            elif type == "LineString":
                self.position_list = []
                points = [[float(lat), float(lon)] for lon, lat in points]
                html = self.ovv_map_data.add_line(type, points)
                points.pop()
                self.position_list = copy.deepcopy(points)
                

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
