import customtkinter as ctk
from pathlib import Path
from tkintermapview import TkinterMapView
import os
import tkinter as tk
from tkinter import filedialog
from inoutfile import read_points_from_file, read_number_from_file
import tkinter
import tkintermapview
import math
import copy
import numpy as np
import os
from chia_luoi import find_path
from chia_dien_tich import chia_dien_tich, chia_luoi, chia_luoi_one
from PIL import Image, ImageTk
import time
from threading import Thread
from math import atan2, degrees
import threading
from calculation_helpers import *


parent_dir = Path(__file__).parent.parent
print(parent_dir)


def main():
    app = ctk.CTk()  # Create the main window
    # app = tk.Tk()
    app.title("Bản đồ Drone")
    app.geometry("1200x800")  # Initial size, but it's resizable
    app.iconbitmap('')

    # Configure the grid layout to allow resizing
    app.grid_columnconfigure(0, weight=1)  # Control panel column
    # Map column, increased weight to expand more
    app.grid_columnconfigure(1, weight=150)
    app.grid_rowconfigure(0, weight=1)

    # Left side control panel
    frame_left = ctk.CTkFrame(master=app, width=10, corner_radius=10)
    frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    # Right side map display and top controls
    frame_right = ctk.CTkFrame(master=app)
    frame_right.grid(row=0, column=1, sticky="nswe")
    frame_right.grid_rowconfigure(1, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)
    # Add another column for the map to expand into
    frame_right.grid_columnconfigure(1, weight=1)
    for i in range(4):  # Configure four columns with equal weight
        frame_right.grid_columnconfigure(i, weight=1)

    # Map widget
    # script_directory = os.path.dirname(os.path.abspath(__file__))
    # database_path = os.path.join(script_directory, "offline_tiles(baithunghiem).db")

    # Set the map normal (offline)
    # map_widget = tkintermapview.TkinterMapView(frame_right, corner_radius=0, use_database_only=True,
    #                        max_zoom=20, database_path=database_path)
    # map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
    # map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    # map_widget.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")  # Increase columnspan for the map to expand

    # Set the map satellite (online)
    map_widget = tkintermapview.TkinterMapView(frame_right, corner_radius=0)
    map_widget.set_tile_server(
        "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    # Increase columnspan for the map to expand
    map_widget.grid(row=1, column=0, columnspan=4,
                    padx=20, pady=20, sticky="nsew")

    # Set the map server and position

    map_widget.set_position(21.0609062, 105.791999817)  # Default position
    # map_widget.set_position(21.064677823616574, 105.79319877446977)  # Default position
    # map_widget.set_position(47.400162, 8.542776)  # Default position

    # load images
    # current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    Drone_image = ImageTk.PhotoImage(Image.open(
        f"{parent_dir}/map/images/Drone.png").resize((20, 20)))
    dot_image = ImageTk.PhotoImage(Image.open(
        f"{parent_dir}/map/images/Dot.png").resize((10, 10)))

    # -----------------------------------------------------------------------------------------------
    x_coords = []
    y_coords = []
    grid_enabled = False
    multi_area = False
    grid_path_enable = False
    position_list = []  # danh sach diem
    marker_list = []  # danh sach marker
    grid_points_markers = []  # danh sach marker cua diem luoi
    rotated_area_list = []
    grid_points_list = []
    grid_points_markers_list = []  # danh sach marker cua tat ca cac khu vuc
    area_grid = []
    number = 0  # dem so diem
    polygon_number = 0  # so da giac
    polygon_list = []  # danh sach cac da giac
    path_list = []  # danh sach duong
    grid_path_list = []  # danh sach duong cua diem luoi
    ordered_grid_points = []  # diem luoi
    drone = 0  # dem so drone
    drone_num = 0  # so drone connected
    drone_position_list = []  # danh sach diem
    drone_marker_list = []  # danh sach marker
    divisions = 0
    # update path
    update_active = False
    current_paths = {}
    latest_markers = {}
    update_active = False  # Initially, updates are not active
    update_thread = None  # Initialize the thread variable
    drone_paths = []  # List to store the paths for each drone
    path_lock = threading.Lock()  # Lock to synchronize access to `drone_paths`
    # Reduce path
    all_filtered_sets = []
    # chia khu vuc
    first_time = True

    # -----------------THÊM ĐIỂM------------------------------------------------------------

    def left_click_event(coordinates_tuple):
        nonlocal number
        print("Left click event with coordinates:", coordinates_tuple)
        number += 1
        latitude, longitude = coordinates_tuple

        marker = map_widget.set_marker(
            latitude, longitude, text="Diem " + str(number))
        marker_list.append(marker)  # tao marker
        position_list.append([latitude, longitude])  # them diem vao danh sach
        print(
            f"Point {number} set at latitude: {latitude}, longitude: {longitude}")

    def open_file():
        nonlocal number
        filename = filedialog.askopenfilename(initialdir=f"{parent_dir}/logs/area/", title="Chọn file",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            x_coords_file, y_coords_file = read_points_from_file(filename)
            x_coords.clear()
            y_coords.clear()
            if x_coords_file and y_coords_file:
                x_coords.extend(x_coords_file)
                y_coords.extend(y_coords_file)

            for x, y in zip(x_coords, y_coords):
                number += 1
                marker = map_widget.set_marker(
                    x, y, text="Diem " + str(number))
                marker_list.append(marker)  # tao marker
                position_list.append([x, y])  # them diem vao danh sach

            print(f"Insert by file")
            for index, position in enumerate(position_list):
                print(
                    f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    def add_point():
        nonlocal number
        x = float(entry_search_1.get())
        y = float(entry_search_2.get())
        number += 1
        position_list.append([x, y])  # them diem vao danh sach
        marker = map_widget.set_marker(x, y, text="Diem" + str(number))
        marker_list.append(marker)  # tao marker
        print(f"\nInsert manually")
        print(f"Point {number} set at latitude: {x}, longitude: {y}")
        entry_search_1.delete(0, tk.END)
        entry_search_2.delete(0, tk.END)

    # -----------------THÊM ĐIỂM DRONE------------------------------------------------------------

    def add_poin_station():
        nonlocal drone
        drone += 1
        x = float(entry_search_1.get())
        y = float(entry_search_2.get())
        drone_position_list.append([x, y])  # them diem vao danh sach
        drone_marker = map_widget.set_marker(
            x, y, text="Drone" + str(drone), icon=Drone_image)
        drone_marker_list.append(drone_marker)  # tao marker
        print(f"\nInsert manually")
        print(f"Drone {drone} set at latitude: {x}, longitude: {y}")
        entry_search_1.delete(0, tk.END)
        entry_search_2.delete(0, tk.END)

    def open_file_drone():
        nonlocal drone, drone_num
        id_drone = []

        if drone != 0:
            for i in range(drone):
                drone_position_list.pop()
                removed_marker = drone_marker_list.pop()
                removed_marker.delete()
                drone -= 1

            if drone < 1:
                print(f"All point deleted")
                drone = 0

        # đọc số  lượng drone
        file_name = f"{parent_dir}/data/drone_num.txt"
        try:
            with open(file_name, 'r') as file:
                # Read the first line and strip any extraneous whitespace
                number_string = file.readline().strip()
                # Convert the string to an integer and return it
                drone_num = int(number_string)
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist.")
        except ValueError:
            print(
                f"Error: The content of the file '{file_name}' is not a valid integer.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print(f"{drone_num}")

        # đọc id drone
        x_coords_file = read_number_from_file()
        x_coords.clear()
        if x_coords_file:
            x_coords.extend(x_coords_file)

        id_drone = sorted(x_coords)

        # đọc vị trí drone
        for i in range(drone_num):
            with open(f'{parent_dir}/logs/gps/gps_data{id_drone[i]}.txt', 'r') as file:
                first_line = file.readline()  # Read only the first line of each file
                # Assuming space-separated x, y coordinates.
                parts = first_line.strip().split(", ")
                if len(parts) >= 2:
                    # Convert string to float for coordinates
                    x, y = float(parts[0]), float(parts[1])
                    drone += 1
                    print(f"{drone}")
                    drone_marker = map_widget.set_marker(
                        x, y, text="Drone " + str(drone), icon=Drone_image)
                    # Adding marker.
                    drone_marker_list.append(drone_marker)
                    # Adding position to the list.
                    drone_position_list.append([x, y])

        # print("Init position list", drone_position_list)

        # filename = filedialog.askopenfilename(initialdir="./", title="Chọn file",
        #                                       filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        # if filename:
        #     x_coords_file, y_coords_file = read_points_from_file(filename)
        #     x_coords.clear()
        #     y_coords.clear()
        #     if x_coords_file and y_coords_file:
        #         x_coords.extend(x_coords_file)
        #         y_coords.extend(y_coords_file)

        #     for x, y in zip(x_coords, y_coords):
        #         drone += 1
        #         drone_marker = map_widget.set_marker(x, y, text= "Drone " + str(drone), icon=Drone_image)
        #         drone_marker_list.append(drone_marker) #tao marker
        #         drone_position_list.append([x, y]) #them diem vao danh sach

        #     print(f"Insert by file")
        #     for index, position in enumerate(drone_position_list):
        #             print(f"Drone {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    # -----------------XÓA ĐIỂM DRONE------------------------------------------------------------

    def clear_poin_station():
        nonlocal drone
        drone_position_list.pop()
        removed_marker = drone_marker_list.pop()
        removed_marker.delete()
        drone -= 1
        if drone < 1:
            print(f"All point deleted")
            drone = 0
        print(f"\nDELETED")
        for index, position in enumerate(drone_position_list):
            print(
                f"Drone {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    # -----------------XÓA ĐIỂM CỨU NẠN------------------------------------------------------------
    def clear_last_point():  # Xóa điểm
        nonlocal number
        position_list.pop()
        removed_marker = marker_list.pop()
        removed_marker.delete()
        number -= 1
        if number < 1:
            print(f"All point deleted\n")
            number = 0
        print(f"\nDELETED")
        for index, position in enumerate(position_list):
            print(
                f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    def clear_path():  # Xóa đường
        path_1 = path_list.pop()
        path_1.delete()

    def clear_polygon():  # Xóa đa giác
        nonlocal polygon_number
        polygon_number -= 1
        polygon1 = polygon_list.pop()
        polygon1.delete()
        print(f"Polygon deleted\n")
        if polygon_number < 1:
            print(f"All polygon deleted\n")
            polygon_number = 0

    # -----------------XUẤT FILE------------------------------------------------------------

    def export_file():
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Lưu file",
                                                initialdir=f"{parent_dir}/logs/points/",
                                                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        diem = copy.deepcopy(position_list)

        # if diem[0] != diem[-1]:
        #     diem.append(diem[0])

        if filename:
            try:
                with open(filename, 'w') as file:
                    for position in diem:
                        file.write(f"{position[0]}, {position[1]}\n")
            except Exception as e:
                print(f"Error writing positions to file: {e}")

    # -----------------THÊM ĐƯỜNG------------------------------------------------------------

    def add_path():
        path_list.append(map_widget.set_path(position_list))

    # -----------------THEO DÕI DRONE------------------------------------------------------------

    def calculate_bearing(lat1, lon1, lat2, lon2):
        # Calculate the difference in coordinates
        delta_x = lon2 - lon1
        delta_y = lat2 - lat1

        # Calculate the angle from the x-axis to the line connecting the points
        angle = math.atan2(delta_y, delta_x)

        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle)

        # Normalize the angle between 0 and 360 degrees
        angle_degrees = (angle_degrees + 360) % 360

        return angle_degrees

    def create_rotated_images(image_path, rotations, size=(50, 50)):
        """Create rotated images at given rotations, resized to the specified size."""
        base_image = Image.open(image_path)
        resized_image = base_image.resize(
            size, Image.LANCZOS)  # High-quality downsampling
        rotated_images = {}
        for angle in rotations:
            # Adjust the angle so 0 degrees corresponds to the x-axis
            adjusted_angle = angle
            # Rotate the image and convert to PhotoImage, negative for clockwise rotation
            rotated_image = resized_image.rotate(adjusted_angle, expand=True)
            rotated_images[angle] = ImageTk.PhotoImage(rotated_image)
        return rotated_images

    # Assuming Drone.png is in the same directory as the script and rotations every 30 degrees
    rotations = range(0, 360, 1)  # 0 to 360 degrees
    rotated_drone_images = create_rotated_images(
        f"{parent_dir}/map/images/Drone.png", rotations, size=(50, 50))

    # Define a list of colors for paths
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
    color_index = 0  # Index to iterate over colors list

    def read_points_update_paths(num_drones, update_interval=2):
        global drone_paths
        nonlocal update_active

        # Initialize paths for each drone
        drone_paths = [[] for _ in range(num_drones)]

        while update_active:
            for i in range(num_drones):
                try:
                    # Read the latest point from each file
                    with open(f'{parent_dir}/logs/gps/gps_data{i+1}.txt', 'r') as file:
                        line = file.readline().strip()
                        if line:
                            lat, lon = map(float, line.split(', '))
                            drone_paths[i].append((lat, lon))

                            # Update the path of the current drone
                            update_drone_path(i)
                except FileNotFoundError:
                    print(f"File for drone {i+1} not found.")
                except Exception as e:
                    print(f"Error reading file for drone {i+1}: {str(e)}")

            # Wait for 2 seconds before reading the next point
            time.sleep(update_interval)

    def update_drone_path(drone_id):
        global drone_paths
        # Assuming drone_paths[drone_id] has at least two points to calculate bearing
        if len(drone_paths[drone_id]) > 1:
            latest_position = drone_paths[drone_id][-2]
            current_position = drone_paths[drone_id][-1]
            yaw = calculate_bearing(
                latest_position[0], latest_position[1], current_position[0], current_position[1])
            closest_angle = min(rotations, key=lambda x: abs(x - yaw))
            icon_image = Drone_image

            # Update marker and path on the map
            if latest_markers.get(drone_id):
                latest_markers[drone_id].delete()
            latest_markers[drone_id] = map_widget.set_marker(
                current_position[0], current_position[1], text=f"Drone {drone_id+1}", icon=icon_image)
            if current_paths.get(drone_id):
                current_paths[drone_id].delete()
            current_paths[drone_id] = map_widget.set_path(
                [p for p in drone_paths[drone_id]], color=colors[drone_id])

    def toggle_path_updates():
        nonlocal drone_num

        nonlocal update_active

        if update_active:
            update_active = False
            print("Updating stopped.")
        else:
            nonlocal drone
            for i in range(drone_num):
                drone_position_list.pop()
                removed_marker = drone_marker_list.pop()
                removed_marker.delete()
                drone -= 1

            if drone < 1:
                print(f"All point deleted")
                drone = 0

            update_active = True
            # Start the thread to read points and update paths
            threading.Thread(target=read_points_update_paths,
                             args=(drone_num,)).start()
            print("Updating started.")

    # def toggle_path_updates():
    #     nonlocal all_filtered_sets
    #     drone_paths = copy.deepcopy(all_filtered_sets)
    #     nonlocal update_active, current_paths, latest_markers

    #     def delete_drone_path(drone_id):
    #         if latest_markers.get(drone_id):
    #             latest_markers[drone_id].delete()
    #             latest_markers[drone_id] = None
    #         if current_paths.get(drone_id):
    #             current_paths[drone_id].delete()
    #             current_paths[drone_id] = None

    #     def add_point_to_path(drone_id, index, marker=None):
    #         nonlocal current_paths, latest_markers
    #         position_list = drone_paths[drone_id]

    #         if index < len(position_list):
    #             latest_position = position_list[index]

    #             if marker:
    #                 marker.delete()

    #             if index + 1 < len(position_list):
    #                 next_position = position_list[index + 1]
    #                 yaw = calculate_bearing(latest_position[0], latest_position[1], next_position[0], next_position[1])
    #                 closest_angle = min(rotations, key=lambda x: abs(x - yaw))
    #                 icon_image = rotated_drone_images[closest_angle]
    #             else:
    #                 icon_image = Drone_image  # Default icon if it's the last point

    #             latest_markers[drone_id] = map_widget.set_marker(latest_position[0], latest_position[1], text=f"Drone {drone_id}", icon=icon_image)

    #             if current_paths.get(drone_id):
    #                 current_paths[drone_id].delete()

    #             if index > 0:
    #                 current_paths[drone_id] = map_widget.set_path(position_list[:index + 1], color='#FFA500')

    #             if index + 1 < len(position_list):
    #                 map_widget.after(2000, lambda: add_point_to_path(drone_id, index + 1, latest_markers[drone_id]))
    #             else:
    #                 print(f"All points for drone {drone_id} have been added to the map.")

    #     if update_active:
    #         # Delete paths for all drones
    #         for drone_id in range(len(drone_paths)):
    #             delete_drone_path(drone_id)
    #         print("Latest markers and paths have been removed.")
    #         update_active = False
    #     else:
    #         drone_position_list.pop()
    #         removed_marker = drone_marker_list.pop()
    #         removed_marker.delete()
    #         # Activate path updates for all drones
    #         for drone_id, _ in enumerate(drone_paths):
    #             if drone_paths[drone_id]:
    #                 add_point_to_path(drone_id, 0)
    #         update_active = True

    # -----------------THÊM ĐA GIÁC------------------------------------------------------------

    def add_polygon():
        nonlocal polygon_number
        polygon_number += 1
        polygon_list.append(map_widget.set_polygon(position_list))
        print(f'POLYGON: {polygon_number}')
        for index, position in enumerate(position_list):
            print(
                f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    # -----------------TÍNH KHOẢNG CÁCH 2 ĐIỂM------------------------------------------------------------

    def distance_list():
        distances = []
        for i in range(len(position_list)):
            if i == (len(position_list)-1):
                lat1, lon1 = position_list[i]
                lat2, lon2 = position_list[0]
            else:
                lat1, lon1 = position_list[i]
                lat2, lon2 = position_list[i + 1]

            distance = haversine(lat1, lon1, lat2, lon2)
            distances.append(distance)

        for index, khoang_cach in enumerate(distances):
            print(f"Distance {index + 1} is: {khoang_cach}")

    # -----------------TÍNH GÓC GIỮA 3 ĐIỂM------------------------------------------------------------

    def calculate_area_and_display():
        goc = find_biggest_angle(position_list)
        canh = distance_list()
        area_m2 = calculate_polygon_area(goc, canh, position_list)
        if area_m2 is not None:
            label_info.configure(text=f"{area_m2:.2f} m2")
        else:
            label_info.configure(text="NaN")

    # -----------------CHIA KHU VỰC------------------------------------------------------------
    def area_division():
        nonlocal polygon_number
        nonlocal grid_points_list
        nonlocal rotated_area_list
        nonlocal drone_num, first_time

        areass = int(drone_num) - 1
        if first_time:
            areas, rotated_area_list = chia_dien_tich(position_list, areass)
        else:
            number = float(entry_area.get())
            areas, rotated_area_list = chia_dien_tich(
                position_list, int(number))

        first_time = False
        grid_points_list = copy.deepcopy(rotated_area_list)
        for i, point in enumerate(areas):
            polygon_list.append(map_widget.set_polygon(point))
            polygon_number += 1
            print(f"POLYGON {polygon_number} ")
            for index, position in enumerate(point):
                print(
                    f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    # -----------------THÊM LƯỚI------------------------------------------------------------

    def toggle_grid():
        nonlocal grid_enabled
        nonlocal multi_area
        nonlocal ordered_grid_points
        nonlocal grid_points_markers_list
        nonlocal area_grid
        nonlocal rotated_area_list
        nonlocal position_list
        grid_points = []

        if grid_enabled or not entry_grid_distance.get():
            # Remove all markers and clear points from the grid
            for grid_points_markers in grid_points_markers_list:
                for marker in grid_points_markers:
                    marker.delete()  # Assuming each marker has a delete method
            # Now clear the lists that were holding the points and markers
            ordered_grid_points.clear()
            grid_points_markers_list.clear()
            area_grid.clear()
            grid_enabled = False

        else:
            distance = float(entry_grid_distance.get())
            # Generate new grid points and add markers
            if not entry_area.get():
                position_list = [tuple(lst) for lst in position_list]
                grid_points = chia_luoi_one(position_list, distance)

                multi_area = False
                print("FALSE 1")
                print(position_list)
                print(grid_points)
            else:
                area = float(entry_area.get())
                if area in (0, 1):
                    position_list = [tuple(lst) for lst in position_list]
                    grid_points = chia_luoi_one(position_list, distance)
                    multi_area = False
                    print("FALSE 2")
                else:
                    grid_points = chia_luoi(rotated_area_list, distance)
                    multi_area = True
                    print("TRUE")

            grid_points_markers_list = []
            area_grid = []
            process_grid_points(grid_points)
            print(f"area_grid {area_grid}")

            # Enable grid
            grid_enabled = True

            # Start writing points to files in another thread
            # threading.Thread(target=write_points_to_files, args=(area_grid,)).start()

    def process_grid_points(grid_points):
        nonlocal area_grid, grid_points_markers_list, ordered_grid_points

        if multi_area:
            for area in grid_points:
                print("AREA", area)
                print(drone_position_list)
                ordered_grid_points = find_path(area, drone_position_list[0])
                print(ordered_grid_points)
                area_marker = create_markers_for_points(ordered_grid_points)
                grid_points_markers_list.append(area_marker)
                area_grid.append(ordered_grid_points)
        else:
            ordered_grid_points = find_path(
                grid_points, drone_position_list[0])
            area_marker = create_markers_for_points(ordered_grid_points)
            grid_points_markers_list.append(area_marker)
            area_grid.append(ordered_grid_points)

    def create_markers_for_points(points):
        area_marker = []
        print("CAC DIEM LUOI")
        for i, point in enumerate(points):
            print(point)
            grid_marker = map_widget.set_marker(
                point[0], point[1], text=" " + str((i+1)), icon=dot_image)
            area_marker.append(grid_marker)
        return area_marker

    def write_points_to_files(area_grid):
        # Determine the maximum length of sublists to handle different lengths
        max_length = max(len(points) for points in area_grid)

        # Loop over each point index in the longest list of points
        for index in range(max_length):
            for i, area_points in enumerate(area_grid):
                # Check if current index is within the length of current area points list
                if index < len(area_points):
                    with open(f'{parent_dir}/points/points{i+1}.txt', 'w') as file:
                        point = area_points[index]
                        # Write the current point
                        file.write(f'{point[0]}, {point[1]}\n')
                        file.truncate()  # Optional: Ensure the file only contains this point

            # After writing the current point for each drone, wait for 2 seconds
            time.sleep(2)

    # def toggle_grid():
    #     nonlocal grid_enabled
    #     nonlocal multi_area
    #     nonlocal ordered_grid_points
    #     nonlocal grid_points_markers_list
    #     nonlocal area_grid
    #     nonlocal rotated_area_list
    #     nonlocal position_list
    #     grid_points =[]

    #     if grid_enabled or entry_grid_distance.get() == '':
    #         # Remove all markers and clear points from the grid
    #         for grid_points_markers in grid_points_markers_list:
    #             for marker in grid_points_markers:
    #                 marker.delete()  # Assuming each marker has a delete method
    #         # Now clear the lists that were holding the points and markers
    #         ordered_grid_points.clear()
    #         grid_points_markers_list.clear()
    #         area_grid.clear()
    #         grid_enabled = False

    #     else:
    #         distance = float(entry_grid_distance.get())
    #         # Generate new grid points and add markers
    #         if entry_area.get() == '':
    #             position_list = [tuple(lst) for lst in position_list]
    #             grid_points = chia_luoi_one(position_list, distance)

    #             multi_area = False
    #             print(f"FALSE 1")
    #             print(f"{position_list}")
    #             print(f"{grid_points}")
    #         else:
    #             if float(entry_area.get()) == 0 or float(entry_area.get()) == 1:
    #                 position_list = [tuple(lst) for lst in position_list]
    #                 grid_points = chia_luoi_one(position_list, distance)
    #                 multi_area = False
    #                 print(f"FALSE 2")
    #             else:
    #                 grid_points = chia_luoi(rotated_area_list, distance)
    #                 multi_area = True
    #                 print(f"TRUE")

    #         grid_points_markers_list = []
    #         area_grid = []
    #         if multi_area:
    #             for area in grid_points:
    #                 print(f"AREA {area}")
    #                 ordered_grid_points = find_path(area, drone_position_list[0])
    #                 print(f"{ordered_grid_points}")
    #                 area_marker = []
    #                 print(f"CAC DIEM LUOI")
    #                 for i, point in enumerate(ordered_grid_points):
    #                     print(f"{point}")
    #                     grid_marker = map_widget.set_marker(point[0], point[1], text= " " + str((i+1)), icon = dot_image)
    #                     area_marker.append(grid_marker)
    #                 grid_points_markers_list.append(area_marker)
    #                 area_grid.append(ordered_grid_points)
    #         else:
    #             ordered_grid_points = find_path(grid_points, drone_position_list[0])
    #             area_marker = []
    #             print(f"CAC DIEM LUOI")
    #             for i, point in enumerate(ordered_grid_points):
    #                 print(f"{point}")
    #                 grid_marker = map_widget.set_marker(point[0], point[1], text= " " + str((i+1)), icon = dot_image)
    #                 area_marker.append(grid_marker)
    #             grid_points_markers_list.append(area_marker)
    #             area_grid.append(ordered_grid_points)

    #         #ordered_grid_points = [point for sublist in grid_points for point in sublist]
    #         grid_enabled = True

    # -----------------XUẤT ĐIỂM LƯỚI------------------------------------------------------------

    def export_grid_points():
        nonlocal area_grid
        print("DAY LA ordered_grid_points")
        print(f"{area_grid}")
        for i in range(len(area_grid)):
            points = area_grid[i]
            print("DAY LA POINTS")
            print(f"{points}")

            with open(f'{parent_dir}logs/gps/gps_data{i+1}.txt', 'r') as file:
                # Read the first line from the file
                first_line = file.readline().strip()

                # Split the line into an array based on the comma separator
                result_array = first_line.split(',')

                # Convert string values to float
                result_array = [float(value) for value in result_array]

            with open(f'{parent_dir}logs/points/points{i+1}.txt', 'w') as file:
                file.write(f"{result_array[0]}, {result_array[1]}\n")
                for pos in points:
                    file.write(f"{pos[0]}, {pos[1]}\n")

    # -----------------RÚT GỌN ĐIỂM LƯỚI------------------------------------------------------------

    def point_on_line(point_a, point_c, point_b, margin_of_error=0.0001):
        """
        Check if point_c lies on the line defined by point_a and point_b
        within a specified margin of error.
        """
        # Calculate distances between the points
        dist_ab = haversine(point_a[0], point_a[1], point_b[0], point_b[1])
        dist_ac = haversine(point_a[0], point_a[1], point_c[0], point_c[1])
        dist_bc = haversine(point_b[0], point_b[1], point_c[0], point_c[1])

        # Check if the sum of distances AC and BC is approximately equal to AB
        return math.isclose(dist_ab, dist_ac + dist_bc, rel_tol=margin_of_error)

    def remove_collinear_points():
        nonlocal all_filtered_sets
        nonlocal area_grid
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

        for i in range(len(all_filtered_sets)):
            points = all_filtered_sets[i]
            print("DAY LA POINTS")
            print(f"{points}")
            with open(f'{parent_dir}/logs/remove/removed{i+1}.txt', 'w') as file:
                for pos in points:
                    file.write(f"{pos[0]}, {pos[1]}\n")

        return all_filtered_sets

    # -----------------VẼ ĐƯỜNG ĐI TRÊN LƯỚI------------------------------------------------------------

    def path_grid_points():
        nonlocal grid_path_enable
        nonlocal area_grid
        nonlocal grid_path_list
        # Define a list of colors for paths
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
        color_index = 0  # Index to iterate over colors list

        if grid_path_enable:
            for i in range(len(area_grid)):
                path_1 = grid_path_list.pop()
                path_1.delete()

            grid_path_enable = False
        else:
            for i in range(len(area_grid)):
                # Set the path color
                color = colors[color_index]
                # Increment color index
                color_index = (color_index + 1) % len(colors)
                points = area_grid[i]
                grid_path_list.append(map_widget.set_path(points, color=color))

            grid_path_enable = True

    # Top control elements in the right frame
    entry_search_1 = ctk.CTkEntry(
        master=frame_right, placeholder_text="Vĩ độ (Latitude)")
    entry_search_1.grid(row=0, column=0, padx=10, pady=10, sticky="we")

    entry_search_2 = ctk.CTkEntry(
        master=frame_right, placeholder_text="Kinh độ (Longitude)")
    entry_search_2.grid(row=0, column=1, padx=10, pady=10, sticky="we")

    button_search = ctk.CTkButton(
        master=frame_right, text="Thêm điểm cứu nạn", command=add_point)
    button_search.grid(row=0, column=2, padx=10, pady=10, sticky="we")

    button_clear_search = ctk.CTkButton(
        master=frame_right, text="Thêm điểm Drone", command=add_poin_station)
    button_clear_search.grid(row=0, column=3, padx=10, pady=10, sticky="we")

    # Left click
    map_widget.add_left_click_map_command(left_click_event)

    # Additional controls in the left frame
    button_add_marker = ctk.CTkButton(
        frame_left, text="Mở file điểm Drone", command=open_file_drone)
    button_add_marker.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xóa điểm Drone", command=clear_poin_station)
    button_add_marker.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Mở file điểm cứu nạn", command=open_file)
    button_add_marker.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xóa điểm cứu nạn", command=clear_last_point)
    button_add_marker.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xuất file điểm cứu nạn", command=export_file)
    button_add_marker.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Tạo đường đi", command=add_path)
    button_add_marker.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xóa đường đi", command=clear_path)
    button_add_marker.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Tạo đa giác", command=add_polygon)
    button_add_marker.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xóa đa giác", command=clear_polygon)
    button_add_marker.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Tính diện tích", command=calculate_area_and_display)
    button_add_marker.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

    # Define a label and place it under the button
    label_info = ctk.CTkLabel(frame_left, text="Diện tích đa giác",
                              corner_radius=10, fg_color="light gray", text_color="gray")
    label_info.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Xuất điểm lưới", command=export_grid_points)
    button_add_marker.grid(row=12, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Vẽ/Xóa đường đi lưới", command=path_grid_points)
    button_add_marker.grid(row=13, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Theo dõi Drone", command=toggle_path_updates)
    button_add_marker.grid(row=14, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Tính khoảng cách", command=distance_list)
    button_add_marker.grid(row=15, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(
        frame_left, text="Rút gọn điểm", command=remove_collinear_points)
    button_add_marker.grid(row=16, column=0, padx=10, pady=10, sticky="ew")

    # New buttons under the existing ones
    button_new_1 = ctk.CTkButton(
        master=frame_right, text="Chia khu vực", command=area_division)
    button_new_1.grid(row=2, column=1, padx=10, pady=10, sticky="we")

    button_new_2 = ctk.CTkButton(
        master=frame_right, text="Bật/Tắt lưới", command=toggle_grid)
    button_new_2.grid(row=2, column=3, padx=10, pady=10, sticky="we")

    entry_area = ctk.CTkEntry(
        master=frame_right, placeholder_text="Số khu vực cần chia")
    entry_area.grid(row=2, column=0, padx=10, pady=10, sticky="we")

    entry_grid_distance = ctk.CTkEntry(
        master=frame_right, placeholder_text="Khoảng cách lưới")
    entry_grid_distance.grid(row=2, column=2, padx=10, pady=10, sticky="we")

    app.mainloop()


if __name__ == "__main__":
    main()
