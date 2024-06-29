import customtkinter as ctk
from tkintermapview import TkinterMapView
import os
import tkinter as tk
from tkinter import filedialog
from inoutfile import read_points_from_file
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
from PIL import Image, ImageTk



def main():
    app = ctk.CTk()  # Create the main window
    app.title("Bản đồ Drone")
    app.geometry("1200x800")  # Initial size, but it's resizable
    app.iconbitmap('')

    # Configure the grid layout to allow resizing
    app.grid_columnconfigure(0, weight=1)  # Control panel column
    app.grid_columnconfigure(1, weight=150)  # Map column, increased weight to expand more
    app.grid_rowconfigure(0, weight=1)

    # Left side control panel
    frame_left = ctk.CTkFrame(master=app, width=10, corner_radius=10)
    frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    # Right side map display and top controls
    frame_right = ctk.CTkFrame(master=app)
    frame_right.grid(row=0, column=1, sticky="nswe")
    frame_right.grid_rowconfigure(1, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_columnconfigure(1, weight=1)  # Add another column for the map to expand into
    for i in range(4):  # Configure four columns with equal weight
        frame_right.grid_columnconfigure(i, weight=1)

    # Map widget
    script_directory = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_directory, "offline_tiles.db")

    # Set the map normal (offline)
    map_widget = tkintermapview.TkinterMapView(frame_right, corner_radius=0, use_database_only=True,
                            max_zoom=20, database_path=database_path)
    map_widget.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")  # Increase columnspan for the map to expand
   
    # Set the map satellite (online)
    # map_widget = tkintermapview.TkinterMapView(frame_right, corner_radius=0)
    # map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    # map_widget.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")  # Increase columnspan for the map to expand

    # Set the map server and position
    map_widget.set_position(21.039507383255135, 105.78272944495943)  # Default position

    

    # load images
    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    Drone_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "Drone.png")).resize((70, 70)))
    dot_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "Dot.png")).resize((10, 10)))

    #-----------------------------------------------------------------------------------------------
    x_coords = []
    y_coords = []
    grid_enabled = False
    multi_area = False
    grid_path_enable = False
    position_list = [] #danh sach diem
    marker_list = [] #danh sach marker
    grid_points_markers = [] #danh sach marker cua diem luoi
    rotated_area_list = []
    grid_points_list = []
    grid_points_markers_list = [] #danh sach marker cua tat ca cac khu vuc
    area_grid =[]
    number = 0 #dem so diem
    polygon_number = 0 #so da giac
    polygon_list = [] #danh sach cac da giac
    path_list = [] #danh sach duong
    grid_path_list = [] #danh sach duong cua diem luoi
    ordered_grid_points =[] #diem luoi
    drone = 0 #dem so drone
    drone_position_list = [] #danh sach diem
    drone_marker_list = [] #danh sach marker
    divisions = 0 
    #update path
    update_active = False
    current_paths = {}
    latest_markers = {}
    #Reduce path 
    all_filtered_sets = []

    #-----------------THÊM ĐIỂM------------------------------------------------------------

    def left_click_event(coordinates_tuple):
        nonlocal number
        print("Left click event with coordinates:", coordinates_tuple)
        number += 1 
        latitude, longitude = coordinates_tuple

        marker = map_widget.set_marker(latitude, longitude, text= "Diem " + str(number))
        marker_list.append(marker) #tao marker
        position_list.append([latitude, longitude]) #them diem vao danh sach
        print(f"Point {number} set at latitude: {latitude}, longitude: {longitude}")
    
    def open_file():
        nonlocal number
        filename = filedialog.askopenfilename(initialdir="./", title="Chọn file",
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
                marker = map_widget.set_marker(x, y, text= "Diem " + str(number))
                marker_list.append(marker) #tao marker
                position_list.append([x, y]) #them diem vao danh sach
                
            print(f"Insert by file")
            for index, position in enumerate(position_list):
                    print(f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")


    def add_point():
        nonlocal number
        x = float(entry_search_1.get())
        y = float(entry_search_2.get())
        number += 1
        position_list.append([x, y]) #them diem vao danh sach
        marker = map_widget.set_marker(x, y, text="Diem" + str(number))
        marker_list.append(marker)#tao marker
        print(f"\nInsert manually")
        print(f"Point {number} set at latitude: {x}, longitude: {y}")
        entry_search_1.delete(0, tk.END)
        entry_search_2.delete(0, tk.END)

    #-----------------THÊM ĐIỂM DRONE------------------------------------------------------------

    def add_poin_station():
        nonlocal drone
        drone += 1
        x = float(entry_search_1.get())
        y = float(entry_search_2.get())
        drone_position_list.append([x, y]) #them diem vao danh sach
        drone_marker = map_widget.set_marker(x, y, text="Drone" + str(drone), icon=Drone_image)
        drone_marker_list.append(drone_marker)#tao marker
        print(f"\nInsert manually")
        print(f"Drone {drone} set at latitude: {x}, longitude: {y}")
        entry_search_1.delete(0, tk.END)
        entry_search_2.delete(0, tk.END)
        


    def open_file_drone():
        nonlocal drone
        filename = filedialog.askopenfilename(initialdir="./", title="Chọn file",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            x_coords_file, y_coords_file = read_points_from_file(filename)
            x_coords.clear()
            y_coords.clear()
            if x_coords_file and y_coords_file:
                x_coords.extend(x_coords_file)
                y_coords.extend(y_coords_file)

            for x, y in zip(x_coords, y_coords):
                drone += 1
                drone_marker = map_widget.set_marker(x, y, text= "Drone " + str(drone), icon=Drone_image)
                drone_marker_list.append(drone_marker) #tao marker
                drone_position_list.append([x, y]) #them diem vao danh sach
                
            print(f"Insert by file")
            for index, position in enumerate(drone_position_list):
                    print(f"Drone {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    
    #-----------------XÓA ĐIỂM DRONE------------------------------------------------------------
        
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
            print(f"Drone {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")
    
    #-----------------XÓA ĐIỂM CỨU NẠN------------------------------------------------------------
    def clear_last_point(): #Xóa điểm
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
                    print(f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    def clear_path():   #Xóa đường
        path_1 = path_list.pop()
        path_1.delete()

    def clear_polygon(): #Xóa đa giác
        nonlocal polygon_number
        polygon_number -= 1
        polygon1 = polygon_list.pop()
        polygon1.delete()
        print(f"Polygon deleted\n")
        if polygon_number < 1:
            print(f"All polygon deleted\n")
            polygon_number = 0
    
    #-----------------XUẤT FILE------------------------------------------------------------
    
    def export_file():
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Lưu file",
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
        

    #-----------------THÊM ĐƯỜNG------------------------------------------------------------
    def add_path():
        path_list.append(map_widget.set_path(position_list))

    #-----------------THEO DÕI DRONE------------------------------------------------------------
    
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
        resized_image = base_image.resize(size, Image.Resampling.LANCZOS)  # High-quality downsampling
        rotated_images = {}
        for angle in rotations:
            # Adjust the angle so 0 degrees corresponds to the x-axis
            adjusted_angle = angle
            # Rotate the image and convert to PhotoImage, negative for clockwise rotation
            rotated_image = resized_image.rotate(adjusted_angle, expand=True)
            rotated_images[angle] = ImageTk.PhotoImage(rotated_image)
        return rotated_images
    
    # Assuming Drone.png is in the same directory as the script and rotations every 30 degrees
    rotations = range(0, 360, 1)  # 0 to 330 degrees
    rotated_drone_images = create_rotated_images("images/Drone.png", rotations, size=(50, 50))


    def toggle_path_updates():
        nonlocal all_filtered_sets
        drone_paths = copy.deepcopy(all_filtered_sets)
        nonlocal update_active, current_paths, latest_markers

        def delete_drone_path(drone_id):
            if latest_markers.get(drone_id):
                latest_markers[drone_id].delete()
                latest_markers[drone_id] = None
            if current_paths.get(drone_id):
                current_paths[drone_id].delete()
                current_paths[drone_id] = None

        def add_point_to_path(drone_id, index, marker=None):
            nonlocal current_paths, latest_markers
            position_list = drone_paths[drone_id]
            
            if index < len(position_list):
                latest_position = position_list[index]

                if marker:
                    marker.delete()

                if index + 1 < len(position_list):
                    next_position = position_list[index + 1]
                    yaw = calculate_bearing(latest_position[0], latest_position[1], next_position[0], next_position[1])
                    closest_angle = min(rotations, key=lambda x: abs(x - yaw))
                    icon_image = rotated_drone_images[closest_angle]
                else:
                    icon_image = Drone_image  # Default icon if it's the last point

                latest_markers[drone_id] = map_widget.set_marker(latest_position[0], latest_position[1], text=f"Drone {drone_id}", icon=icon_image)

                if current_paths.get(drone_id):
                    current_paths[drone_id].delete()

                if index > 0:
                    current_paths[drone_id] = map_widget.set_path(position_list[:index + 1], color='#FFA500')

                if index + 1 < len(position_list):
                    map_widget.after(2000, lambda: add_point_to_path(drone_id, index + 1, latest_markers[drone_id]))
                else:
                    print(f"All points for drone {drone_id} have been added to the map.")

        if update_active:
            # Delete paths for all drones
            for drone_id in range(len(drone_paths)):
                delete_drone_path(drone_id)
            print("Latest markers and paths have been removed.")
            update_active = False
        else:
            drone_position_list.pop()
            removed_marker = drone_marker_list.pop()
            removed_marker.delete()
            # Activate path updates for all drones
            for drone_id, _ in enumerate(drone_paths):
                if drone_paths[drone_id]:
                    add_point_to_path(drone_id, 0)
            update_active = True


 
    #-----------------THÊM ĐA GIÁC------------------------------------------------------------
    def add_polygon():
        nonlocal polygon_number
        polygon_number += 1
        polygon_list.append(map_widget.set_polygon(position_list))
        print(f'POLYGON: {polygon_number}')
        for index, position in enumerate(position_list):
            print(f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")

    #-----------------TÍNH KHOẢNG CÁCH 2 ĐIỂM------------------------------------------------------------
                    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6378000  # bán kính Trái Đất (đơn vị: m)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
    
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
    
    #-----------------TÍNH GÓC GIỮA 3 ĐIỂM------------------------------------------------------------
    def calculate_angle(a, b, c):
        """Calculate angle at b given points a, b, c, including reflex angles."""
        ba = (a[0] - b[0], a[1] - b[1])
        bc = (c[0] - b[0], c[1] - b[1])

        # Dot product
        dot_prod = ba[0] * bc[0] + ba[1] * bc[1]
        # Magnitude of vector AB and BC
        mag_ab = math.sqrt(ba[0]**2 + ba[1]**2)
        mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

        if mag_ab == 0 or mag_bc == 0:
            # Return an angle of 0 or handle it as needed
            return 0
        
        cosine_angle = (dot_prod) / (mag_ab * mag_bc)
        angle = math.acos(cosine_angle)
        # Calculate the cross product of vectors ba and bc
        cross_product = ba[0] * bc[1] - ba[1] * bc[0]
        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle)
        # If the cross product is negative, the angle is reflex, so we adjust the angle
        if cross_product > 0:
            angle_degrees = 360 - angle_degrees
        return angle_degrees

    #-----------------TÍNH DIỆN TÍCH------------------------------------------------------------

    def heron_formula(a, b, c):
        """Apply Heron's formula to calculate the area of a triangle given its side lengths."""
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area
    
    
    def angle_list():
        angles = []
        N = len(position_list)
        for i in range(len(position_list)):
            if i == 0:
                a = position_list[N - 1]  # Previous vertex
                b = position_list[i]      # Current vertex
                c = position_list[(i + 1) % len(position_list)]  # Next vertex, using modulo for circular indexing
                print(f"a= {a} b= {b} c= {c}")
            elif i == (len(position_list) - 1):
                a = position_list[i - 1]  # Previous vertex
                b = position_list[i]      # Current vertex
                c = position_list[0]
                print(f"a= {a} b= {b} c= {c}")
            else:
                a = position_list[i - 1]  # Previous vertex
                b = position_list[i]      # Current vertex
                c = position_list[(i + 1) % len(position_list)]  # Next vertex, using modulo for circular indexing

            angle = calculate_angle(a, b, c)
            angles.append(angle)
        
        for index, goc in enumerate(angles):
                    print(f"Angle {index + 1} is: {goc}")
    
    def find_biggest_angle(points):
        """Find the biggest angle in the polygon made up of positions, correctly identifying reflex angles."""
        angles = []
        N = len(points)
        for i in range(len(points)):
            if i == 0:
                a = points[N - 1]  # Previous vertex
                b = points[i]      # Current vertex
                c = points[(i + 1) % len(points)]  # Next vertex, using modulo for circular indexing
                print(f"a= {a} b= {b} c= {c}")
            elif i == (len(points) - 1):
                a = points[i - 1]  # Previous vertex
                b = points[i]      # Current vertex
                c = points[0]
                print(f"a= {a} b= {b} c= {c}")
            else:
                a = points[i - 1]  # Previous vertex
                b = points[i]      # Current vertex
                c = points[(i + 1) % len(points)]  # Next vertex, using modulo for circular indexing
            
            angle = calculate_angle(a, b, c)
            angles.append(angle)

        return angles

    def calculate_polygon_area(sides, angles, points):
        angles = find_biggest_angle(position_list) # Tính các góc của đa giác
        # Find the index of the largest angle
        index_of_largest_angle = angles.index(max(angles)) #tìm ra góc lớn nhất
        print(f"index_of_largest_angle is: {index_of_largest_angle}")
        
        # Calculate areas of triangles formed with the vertex of the largest angle
        total_area = 0
        n = len(sides)
        for i in range(n):
            if i != index_of_largest_angle and (i + 1) % n != index_of_largest_angle:
                distances =[]
                # Calculate the sides of the triangle
                a = points[index_of_largest_angle]
                b = points[i]
                c = points[(i + 1) % n]
                print(f"a= {a} b= {b} c= {c}")
                canh = [a,b,c]
                for i in range(len(canh)):
                    for j in range(i + 1, len(canh)):
                        distance = haversine(canh[i][0], canh[i][1], canh[j][0], canh[j][1])
                        distances.append(distance)
                        print(f"Distance between point {i+1} and point {j+1} is: {distance}")
                
                
                # Calculate area using Heron's formula
                area = heron_formula(distances[0], distances[1], distances[2])
                print(f"Triangle {i} is: {area}")
                total_area += area
        
        return total_area
    
    def calculate_area_and_display():
        goc = find_biggest_angle(position_list)
        canh = distance_list()
        area_m2 = calculate_polygon_area(goc,canh,position_list)
        if area_m2 is not None:
            label_info.configure(text=f"{area_m2:.2f} m2")
        else:
            label_info.configure(text="NaN")
        
    #-----------------CHIA KHU VỰC------------------------------------------------------------
    def area_division():
        nonlocal polygon_number
        nonlocal grid_points_list
        nonlocal rotated_area_list
        number = float(entry_area.get())
        areas, rotated_area_list= chia_dien_tich(position_list, int(number))
        grid_points_list = copy.deepcopy(rotated_area_list)
        for i, point in enumerate(areas):
            polygon_list.append(map_widget.set_polygon(point))
            polygon_number +=1
            print(f"POLYGON {polygon_number} ")
            for index, position in enumerate(point):
                print(f"Point {index + 1} set at latitude: {position[0]}, longitude: {position[1]}")
        return float(entry_area.get())
    
    #-----------------THÊM LƯỚI------------------------------------------------------------

    def toggle_grid():
        nonlocal grid_enabled
        nonlocal multi_area
        nonlocal ordered_grid_points
        nonlocal grid_points_markers_list
        nonlocal area_grid
        nonlocal rotated_area_list
        nonlocal position_list 
        grid_points =[]

        if grid_enabled or entry_grid_distance.get() == '':
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
            if entry_area.get() == '':
                position_list = [tuple(lst) for lst in position_list]
                grid_points = chia_luoi_one(position_list, distance)
                
                multi_area = False 
                print(f"FALSE 1")
                print(f"{position_list}")
                print(f"{grid_points}")
            else:
                if float(entry_area.get()) == 0 or float(entry_area.get()) == 1:
                    position_list = [tuple(lst) for lst in position_list]
                    grid_points = chia_luoi_one(position_list, distance)
                    multi_area = False 
                    print(f"FALSE 2")
                else:
                    grid_points = chia_luoi(rotated_area_list, distance)
                    multi_area = True 
                    print(f"TRUE")

            grid_points_markers_list = []
            area_grid = []
            if multi_area:
                for area in grid_points:
                    print(f"AREA {area}")
                    ordered_grid_points = find_path(area, drone_position_list[0])
                    print(f"{ordered_grid_points}")
                    area_marker = []
                    print(f"CAC DIEM LUOI")
                    for i, point in enumerate(ordered_grid_points):
                        print(f"{point}")
                        grid_marker = map_widget.set_marker(point[0], point[1], text= " " + str((i+1)), icon = dot_image)
                        area_marker.append(grid_marker)
                    grid_points_markers_list.append(area_marker)
                    area_grid.append(ordered_grid_points)
            else:
                ordered_grid_points = find_path(grid_points, drone_position_list[0])
                area_marker = []
                print(f"CAC DIEM LUOI")
                for i, point in enumerate(ordered_grid_points):
                    print(f"{point}")
                    grid_marker = map_widget.set_marker(point[0], point[1], text= " " + str((i+1)), icon = dot_image)
                    area_marker.append(grid_marker)
                grid_points_markers_list.append(area_marker)
                area_grid.append(ordered_grid_points)

            #ordered_grid_points = [point for sublist in grid_points for point in sublist]
            grid_enabled = True

    #-----------------XUẤT ĐIỂM LƯỚI------------------------------------------------------------
    
    def export_grid_points(): 
        nonlocal area_grid
        print("DAY LA ordered_grid_points")
        print(f"{area_grid}")
        for i in range(len(area_grid)):
            points = area_grid[i]
            print("DAY LA POINTS")
            print(f"{points}")
            with open(f'points{i+1}.txt', 'w') as file:
                for pos in points:
                    file.write(f"{pos[0]}, {pos[1]}\n")
    
    #-----------------RÚT GỌN ĐIỂM LƯỚI------------------------------------------------------------

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
                with open(f'removed{i+1}.txt', 'w') as file:
                    for pos in points:
                        file.write(f"{pos[0]}, {pos[1]}\n")
        
        return all_filtered_sets
    
    
    #-----------------VẼ ĐƯỜNG ĐI TRÊN LƯỚI------------------------------------------------------------
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
                color_index = (color_index + 1) % len(colors)  # Increment color index
                points = area_grid[i]
                grid_path_list.append(map_widget.set_path(points, color = color))
            
            grid_path_enable = True 




    # Top control elements in the right frame
    entry_search_1 = ctk.CTkEntry(master=frame_right, placeholder_text="Vĩ độ (Latitude)")
    entry_search_1.grid(row=0, column=0, padx=10, pady=10, sticky="we")

    entry_search_2 = ctk.CTkEntry(master=frame_right, placeholder_text="Kinh độ (Longitude)")
    entry_search_2.grid(row=0, column=1, padx=10, pady=10, sticky="we")

    button_search = ctk.CTkButton(master=frame_right, text="Thêm điểm cứu nạn", command=add_point)
    button_search.grid(row=0, column=2, padx=10, pady=10, sticky="we")

    button_clear_search = ctk.CTkButton(master=frame_right, text="Thêm điểm Drone", command=add_poin_station)
    button_clear_search.grid(row=0, column=3, padx=10, pady=10, sticky="we")
    
    #Left click
    map_widget.add_left_click_map_command(left_click_event)

    # Additional controls in the left frame
    button_add_marker = ctk.CTkButton(frame_left, text="Mở file điểm Drone", command=open_file_drone)
    button_add_marker.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xóa điểm Drone", command=clear_poin_station)
    button_add_marker.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Mở file điểm cứu nạn", command=open_file)
    button_add_marker.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xóa điểm cứu nạn", command=clear_last_point)
    button_add_marker.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xuất file điểm cứu nạn", command=export_file)
    button_add_marker.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Tạo đường đi", command = add_path)
    button_add_marker.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xóa đường đi", command=clear_path)
    button_add_marker.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Tạo đa giác", command = add_polygon)
    button_add_marker.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xóa đa giác", command=clear_polygon)
    button_add_marker.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Tính diện tích", command=calculate_area_and_display)
    button_add_marker.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

    
    

    # Define a label and place it under the button
    label_info = ctk.CTkLabel(frame_left, text="Diện tích đa giác",corner_radius=10, fg_color="light gray", text_color="gray")
    label_info.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Xuất điểm lưới", command = export_grid_points)
    button_add_marker.grid(row=12, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Vẽ/Xóa đường đi lưới", command = path_grid_points)
    button_add_marker.grid(row=13, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Theo dõi Drone", command = toggle_path_updates)
    button_add_marker.grid(row=14, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Tính khoảng cách", command = distance_list)
    button_add_marker.grid(row=15, column=0, padx=10, pady=10, sticky="ew")

    button_add_marker = ctk.CTkButton(frame_left, text="Rút gọn điểm", command = remove_collinear_points)
    button_add_marker.grid(row=16, column=0, padx=10, pady=10, sticky="ew")

    # New buttons under the existing ones
    button_new_1 = ctk.CTkButton(master=frame_right, text="Chia khu vực", command= area_division)
    button_new_1.grid(row=2, column=1, padx=10, pady=10, sticky="we")

    button_new_2 = ctk.CTkButton(master=frame_right, text="Bật/Tắt lưới", command= toggle_grid)
    button_new_2.grid(row=2, column=3, padx=10, pady=10, sticky="we")

    entry_area = ctk.CTkEntry(master=frame_right, placeholder_text="Số khu vực cần chia")
    entry_area.grid(row=2, column=0, padx=10, pady=10, sticky="we")

    entry_grid_distance = ctk.CTkEntry(master=frame_right, placeholder_text="Khoảng cách lưới")
    entry_grid_distance.grid(row=2, column=2, padx=10, pady=10, sticky="we")



    app.mainloop()

if __name__ == "__main__":
    main()